# Pin Terraform and the AWS provider, so this plans the same way next year as it does today
terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.72"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# The database password comes from outside the code, never from the file itself
variable "database_password" {
  type      = string
  sensitive = true
}

# Load balancer security group: accepts web traffic from anywhere
resource "aws_security_group" "load_balancer" {
  name   = "load-balancer"
  vpc_id = "vpc-0123456789abcdef0"

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# API security group: accepts traffic only from the load balancer
resource "aws_security_group" "api" {
  name   = "api"
  vpc_id = "vpc-0123456789abcdef0"

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.load_balancer.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Database security group: accepts PostgreSQL traffic only from the API tier
resource "aws_security_group" "database" {
  name   = "database"
  vpc_id = "vpc-0123456789abcdef0"

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id]
  }
}

# Load balancer in the public subnets that spreads requests across the API instances
resource "aws_lb" "api" {
  name               = "api-load-balancer"
  internal           = false
  load_balancer_type = "application"
  subnets            = ["subnet-0123456789abcdef0", "subnet-0fedcba9876543210"]
  security_groups    = [aws_security_group.load_balancer.id]
}

# The group of API instances the load balancer sends traffic to, checked for health
resource "aws_lb_target_group" "api" {
  name     = "api-instances"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = "vpc-0123456789abcdef0"

  health_check {
    path = "/health"
  }
}

# Listener that accepts encrypted traffic and forwards it to the API instances
resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.api.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = "arn:aws:acm:us-east-1:123456789012:certificate/00000000-0000-0000-0000-000000000000"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

# Listener that sends anyone using plain HTTP to the HTTPS address
resource "aws_lb_listener" "http_redirect" {
  load_balancer_arn = aws_lb.api.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = "redirect"

    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

# Blueprint for each API instance
resource "aws_launch_template" "api" {
  name_prefix            = "api-"
  image_id               = "ami-0123456789abcdef0"
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.api.id]

  # Require IMDSv2 tokens, so a forged request through the app can't read the instance's credentials
  metadata_options {
    http_tokens = "required"
  }
}

# API tier in the private subnets: two to six instances, replaced if they fail the health check
resource "aws_autoscaling_group" "api" {
  min_size                  = 2
  max_size                  = 6
  desired_capacity          = 2
  vpc_zone_identifier       = ["subnet-0aa11bb22cc33dd44", "subnet-0ee55ff66aa77bb88"]
  target_group_arns         = [aws_lb_target_group.api.arn]
  health_check_type         = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.api.id
    version = "$Latest"
  }
}

# Scaling rule: add or remove instances to keep average CPU near 60 percent
resource "aws_autoscaling_policy" "api_cpu" {
  name                   = "api-cpu"
  autoscaling_group_name = aws_autoscaling_group.api.name
  policy_type            = "TargetTrackingScaling"

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 60
  }
}

# Private subnets the database runs in, the same ones as the API tier
resource "aws_db_subnet_group" "database" {
  name       = "database"
  subnet_ids = ["subnet-0aa11bb22cc33dd44", "subnet-0ee55ff66aa77bb88"]
}

# Primary PostgreSQL database, which handles every write
resource "aws_db_instance" "primary" {
  identifier              = "renovation-primary"
  engine                  = "postgres"
  engine_version          = "18"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  db_name                 = "renovation"
  username                = "app_admin"
  password                = var.database_password
  db_subnet_group_name    = aws_db_subnet_group.database.name
  vpc_security_group_ids  = [aws_security_group.database.id]
  backup_retention_period = 7
  storage_encrypted       = true
  skip_final_snapshot     = true # sandbox only; keep a final snapshot in production
}

# Read replica that takes read traffic off the primary
resource "aws_db_instance" "replica" {
  identifier             = "renovation-replica"
  replicate_source_db    = aws_db_instance.primary.identifier
  instance_class         = "db.t3.micro"
  vpc_security_group_ids = [aws_security_group.database.id]
  skip_final_snapshot    = true
}

"""Checks the case study reference in case-study-reference/ so the published versions stay correct
and in step. Run it from the repo folder after changing any file there:

    python3 tools/check_examples.py

It does two things.

1. Runs each format's own checker, when it is installed:
     Terraform        terraform validate (or tofu validate), else a parse with python-hcl2
     Ansible          ansible-playbook --syntax-check and ansible-lint --profile production
     CloudFormation   cfn-lint
     gRPC             protoc, through grpcio-tools
     GraphQL          graphql-core
     REST (OpenAPI)   openapi-spec-validator
     Messaging        the official AsyncAPI parser (tools/check_asyncapi.mjs, after npm install)
     API server       its own tests (case-study-reference/code/server/tests), which run every request in
                      the example files and check every response against openapi.yaml and asyncapi.yaml

   Install them with:
     pip install python-hcl2 ansible ansible-lint cfn-lint graphql-core openapi-spec-validator
     pip install -r case-study-reference/code/server/requirements.txt
     npm install
   Terraform itself comes from https://developer.hashicorp.com/terraform/install

2. Reads the Terraform, Ansible, and CloudFormation versions of the case study's infrastructure into the
   same shape and compares them setting by setting (ports, sources, sizes, names, the HTTPS redirect,
   scaling limits, database settings). The Terraform is the one printed in the book, so it is the
   reference; any difference in the other two is a failure.

It prints what it found, then PASSED or FAILED, and exits with 1 on any failure.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_FOLDER = Path(__file__).resolve().parent.parent
CASE_STUDY_FOLDER = REPO_FOLDER / "case-study-reference"
IAC_FOLDER = CASE_STUDY_FOLDER / "infrastructure"
API_FOLDER = CASE_STUDY_FOLDER / "code"
TERRAFORM_PATH = IAC_FOLDER / "terraform" / "main.tf"
ANSIBLE_PATH = IAC_FOLDER / "ansible" / "playbook.yml"
CLOUDFORMATION_PATH = IAC_FOLDER / "cloudformation" / "template.yaml"

failures = []
skipped = []


def report(passed, label, detail=""):
    marker = "ok  " if passed else "FAIL"
    print("  " + marker + " " + label + (": " + detail if detail else ""))
    if not passed:
        failures.append(label + (": " + detail if detail else ""))


def run_command(label, command, working_folder):
    if shutil.which(command[0]) is None:
        skipped.append(label + " (" + command[0] + " not installed)")
        print("  skip " + label + " (" + command[0] + " not installed)")
        return
    completed = subprocess.run(command, cwd=working_folder, capture_output=True, text=True)
    output_text = (completed.stdout + completed.stderr).strip()
    report(completed.returncode == 0, label, "" if completed.returncode == 0 else output_text[-1500:])


# ---------- 1. Each format's own checker ----------

def check_terraform():
    terraform_command = shutil.which("terraform") or shutil.which("tofu")
    if terraform_command:
        with tempfile.TemporaryDirectory() as scratch_folder:
            shutil.copy(TERRAFORM_PATH, scratch_folder)
            init_result = subprocess.run([terraform_command, "init", "-backend=false", "-input=false"],
                                         cwd=scratch_folder, capture_output=True, text=True)
            if init_result.returncode != 0:
                report(False, "terraform init", init_result.stderr[-1500:])
                return
            run_command("terraform validate", [terraform_command, "validate"], scratch_folder)
        return
    try:
        import hcl2
    except ImportError:
        skipped.append("Terraform (neither terraform nor python-hcl2 installed)")
        print("  skip Terraform (neither terraform nor python-hcl2 installed)")
        return
    with open(TERRAFORM_PATH) as terraform_file:
        hcl2.load(terraform_file)
    report(True, "Terraform parses", "install terraform for a full terraform validate")


def check_ansible():
    run_command("ansible-playbook --syntax-check",
                ["ansible-playbook", "--syntax-check", ANSIBLE_PATH.name], ANSIBLE_PATH.parent)
    run_command("ansible-lint (production profile)",
                ["ansible-lint", "--profile", "production", "--offline", ANSIBLE_PATH.name], ANSIBLE_PATH.parent)


def check_cloudformation():
    run_command("cfn-lint", ["cfn-lint", CLOUDFORMATION_PATH.name], CLOUDFORMATION_PATH.parent)


def check_protobuf():
    try:
        from grpc_tools import protoc
    except ImportError:
        skipped.append("protoc (grpcio-tools not installed)")
        print("  skip protoc (grpcio-tools not installed)")
        return
    import grpc_tools
    standard_proto_folder = Path(grpc_tools.__file__).resolve().parent / "_proto"
    with tempfile.TemporaryDirectory() as output_folder:
        exit_code = protoc.main(["protoc", "-I" + str(API_FOLDER), "-I" + str(standard_proto_folder),
                                 "--python_out=" + output_folder, str(API_FOLDER / "contractor.proto")])
    report(exit_code == 0, "protoc compiles contractor.proto")


def check_graphql():
    try:
        from graphql import build_schema
    except ImportError:
        skipped.append("GraphQL (graphql-core not installed)")
        print("  skip GraphQL (graphql-core not installed)")
        return
    try:
        build_schema((API_FOLDER / "schema.graphql").read_text())
        report(True, "GraphQL schema builds")
    except Exception as schema_error:
        report(False, "GraphQL schema builds", str(schema_error))


def check_openapi():
    try:
        from openapi_spec_validator import validate
        from openapi_spec_validator.readers import read_from_filename
    except ImportError:
        skipped.append("OpenAPI (openapi-spec-validator not installed)")
        print("  skip OpenAPI (openapi-spec-validator not installed)")
        return
    try:
        specification, _ = read_from_filename(str(API_FOLDER / "openapi.yaml"))
        validate(specification)
        report(True, "OpenAPI description is valid")
    except Exception as specification_error:
        report(False, "OpenAPI description is valid", str(specification_error)[:1500])


def check_asyncapi():
    parser_folder = REPO_FOLDER / "node_modules" / "@asyncapi" / "parser"
    if shutil.which("node") is None or not parser_folder.exists():
        skipped.append("AsyncAPI (run npm install)")
        print("  skip AsyncAPI (run npm install)")
        return
    run_command("AsyncAPI parser", ["node", "tools/check_asyncapi.mjs",
                                    str(API_FOLDER / "messaging" / "asyncapi.yaml")], REPO_FOLDER)


def check_api_server():
    server_folder = API_FOLDER / "server"
    try:
        # Only checking they're installed.
        import ariadne  # noqa: F401
        import grpc_status  # noqa: F401
        import pytest  # noqa: F401
        import starlette  # noqa: F401
    except ImportError as missing_module:
        skipped.append("API server tests (" + str(missing_module) + ")")
        print("  skip API server tests (pip install -r case-study-reference/code/server/requirements.txt)")
        return
    completed = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                               cwd=server_folder, capture_output=True, text=True)
    summary = completed.stdout.strip().split("\n")[-1] if completed.stdout.strip() else ""
    report(completed.returncode == 0, "API server tests", summary if completed.returncode == 0 else completed.stdout[-2500:])


# ---------- 2. Same plan in all three ----------
# Each reader returns the same dictionary shape, so the three can be compared key by key.

def security_group_rules(rules, source_names):
    """Turns ingress rules into sorted (port, source) pairs; sources are a CIDR or a group name."""
    rule_pairs = []
    for rule in rules:
        rule_pairs.append((rule["port"], source_names.get(rule["source"], rule["source"])))
    return sorted(rule_pairs)


def unwrap_old_format(settings, old_format=None):
    """Older python-hcl2 releases (and the one checkov installs) wrap every value in a one-item list
    and add __start_line__ keys to each resource. This unwraps them, so both formats read the same way."""
    if not isinstance(settings, dict):
        return settings
    if old_format is None:
        old_format = "__start_line__" in settings
    unwrapped = {}
    for key, value in settings.items():
        if key in ("__start_line__", "__end_line__"):
            continue
        if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            unwrapped[key] = [unwrap_old_format(item, old_format) for item in value]
        elif old_format and isinstance(value, list) and len(value) == 1:
            unwrapped[key] = value[0]
        else:
            unwrapped[key] = value
    return unwrapped


def read_terraform():
    import hcl2
    with open(TERRAFORM_PATH) as terraform_file:
        parsed = hcl2.load(terraform_file)
    resources = {}
    for resource_block in parsed["resource"]:
        for resource_type, named_blocks in resource_block.items():
            for resource_name, settings in named_blocks.items():
                resources[resource_type.strip('"') + "." + resource_name.strip('"')] = unwrap_old_format(settings)

    def unquote(value):
        return value.strip('"') if isinstance(value, str) else value

    def first_block(value):
        """Nested blocks come back as a list of one block or as the block itself, depending on the version."""
        return value[0] if isinstance(value, list) else value

    def blocks(value):
        if value is None:
            return []
        return value if isinstance(value, list) else [value]

    def reference_name(expression):
        # "${aws_security_group.api.id}" -> "aws_security_group.api"
        inner = expression.strip("${}")
        return ".".join(inner.split(".")[:2])

    group_names = {}
    for key, settings in resources.items():
        if key.startswith("aws_security_group."):
            group_names[key] = unquote(settings["name"])

    security_groups = {}
    for key, settings in resources.items():
        if not key.startswith("aws_security_group."):
            continue
        ingress_rules = []
        for ingress in blocks(settings.get("ingress")):
            for cidr in ingress.get("cidr_blocks", []):
                ingress_rules.append({"port": int(ingress["from_port"]), "source": unquote(cidr)})
            for group_reference in ingress.get("security_groups", []):
                ingress_rules.append({"port": int(ingress["from_port"]),
                                      "source": group_names[reference_name(group_reference)]})
        open_egress = any(unquote(egress.get("protocol")) == "-1" for egress in blocks(settings.get("egress")))
        security_groups[group_names[key]] = {"ingress": security_group_rules(ingress_rules, {}),
                                             "open_egress": open_egress}

    load_balancer = resources["aws_lb.api"]
    target_group = resources["aws_lb_target_group.api"]
    https_listener = resources["aws_lb_listener.https"]
    redirect_listener = resources["aws_lb_listener.http_redirect"]
    redirect = first_block(first_block(redirect_listener["default_action"])["redirect"])
    launch_template = resources["aws_launch_template.api"]
    autoscaling_group = resources["aws_autoscaling_group.api"]
    scaling_policy = first_block(resources["aws_autoscaling_policy.api_cpu"]["target_tracking_configuration"])
    subnet_group = resources["aws_db_subnet_group.database"]
    primary = resources["aws_db_instance.primary"]
    replica = resources["aws_db_instance.replica"]

    return {
        "security_groups": security_groups,
        "load_balancer": {
            "name": unquote(load_balancer["name"]),
            "internet_facing": not load_balancer["internal"],
            "subnets": sorted(unquote(subnet) for subnet in load_balancer["subnets"]),
            "security_groups": sorted(group_names[reference_name(group)] for group in load_balancer["security_groups"]),
        },
        "target_group": {
            "name": unquote(target_group["name"]),
            "port": int(target_group["port"]),
            "protocol": unquote(target_group["protocol"]),
            "health_check_path": unquote(first_block(target_group["health_check"])["path"]),
        },
        "https_listener": {
            "port": int(https_listener["port"]),
            "protocol": unquote(https_listener["protocol"]),
            "ssl_policy": unquote(https_listener["ssl_policy"]),
            "certificate": unquote(https_listener["certificate_arn"]),
            "action": unquote(first_block(https_listener["default_action"])["type"]),
        },
        "redirect_listener": {
            "port": int(redirect_listener["port"]),
            "protocol": unquote(redirect_listener["protocol"]),
            "redirect_to": (str(unquote(redirect["port"])), unquote(redirect["protocol"]), unquote(redirect["status_code"])),
        },
        "launch_template": {
            "image": unquote(launch_template["image_id"]),
            "instance_type": unquote(launch_template["instance_type"]),
            "security_groups": sorted(group_names[reference_name(group)] for group in launch_template["vpc_security_group_ids"]),
            "metadata_tokens": unquote(first_block(launch_template.get("metadata_options", {})).get("http_tokens", "optional")),
        },
        "autoscaling_group": {
            "min": int(autoscaling_group["min_size"]),
            "max": int(autoscaling_group["max_size"]),
            "desired": int(autoscaling_group["desired_capacity"]),
            "subnets": sorted(unquote(subnet) for subnet in autoscaling_group["vpc_zone_identifier"]),
            "health_check_type": unquote(autoscaling_group.get("health_check_type", "EC2")),
            "health_check_grace_seconds": int(autoscaling_group.get("health_check_grace_period", 300)),
        },
        "scaling_policy": {
            "metric": unquote(first_block(scaling_policy["predefined_metric_specification"])["predefined_metric_type"]),
            "target": int(scaling_policy["target_value"]),
        },
        "database_subnets": sorted(unquote(subnet) for subnet in subnet_group["subnet_ids"]),
        "primary_database": {
            "identifier": unquote(primary["identifier"]),
            "engine": unquote(primary["engine"]),
            "engine_version": unquote(primary.get("engine_version", "unpinned")),
            "instance_class": unquote(primary["instance_class"]),
            "storage": int(primary["allocated_storage"]),
            "database_name": unquote(primary["db_name"]),
            "username": unquote(primary["username"]),
            "password_from_outside": unquote(primary["password"]).startswith("${var."),
            "backup_days": int(primary["backup_retention_period"]),
            "encrypted": bool(primary["storage_encrypted"]),
            "security_groups": sorted(group_names[reference_name(group)] for group in primary["vpc_security_group_ids"]),
        },
        "replica_database": {
            "identifier": unquote(replica["identifier"]),
            "source": unquote(primary["identifier"]),
            "instance_class": unquote(replica["instance_class"]),
            "security_groups": sorted(group_names[reference_name(group)] for group in replica["vpc_security_group_ids"]),
        },
    }


def read_ansible():
    import yaml
    playbook = yaml.safe_load(ANSIBLE_PATH.read_text())[0]
    playbook_variables = playbook["vars"]
    tasks_by_module = {}
    for task in playbook["tasks"]:
        module_name = [key for key in task if "." in key][0]
        tasks_by_module.setdefault(module_name, []).append(task)

    def fill(value):
        """Replaces "{{ variable }}" with the playbook's own value, and register names with group names."""
        if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
            expression = value.strip("{} ")
            if expression in playbook_variables:
                return playbook_variables[expression]
            if expression in registered_names:
                return registered_names[expression]
            return expression
        return value

    registered_names = {}
    security_groups = {}
    for task in tasks_by_module["amazon.aws.ec2_security_group"]:
        settings = task["amazon.aws.ec2_security_group"]
        registered_names[task["register"] + ".group_id"] = settings["name"]
    for task in tasks_by_module["amazon.aws.ec2_security_group"]:
        settings = task["amazon.aws.ec2_security_group"]
        ingress_rules = []
        for rule in settings.get("rules", []):
            source = rule.get("cidr_ip") or fill(rule.get("group_id"))
            for port in rule["ports"]:
                ingress_rules.append({"port": int(port), "source": source})
        open_egress = any(rule.get("proto") in ("all", "-1") and rule.get("cidr_ip") == "0.0.0.0/0"
                          for rule in settings.get("rules_egress", []))
        security_groups[settings["name"]] = {"ingress": security_group_rules(ingress_rules, {}),
                                             "open_egress": open_egress}

    target_group_task = tasks_by_module["community.aws.elb_target_group"][0]
    registered_names[target_group_task["register"] + ".target_group_arn"] = target_group_task["community.aws.elb_target_group"]["name"]
    target_group = target_group_task["community.aws.elb_target_group"]
    load_balancer = tasks_by_module["amazon.aws.elb_application_lb"][0]["amazon.aws.elb_application_lb"]
    listeners = {listener["Port"]: listener for listener in load_balancer["listeners"]}
    https_listener = listeners[443]
    redirect_listener = listeners[80]
    redirect = redirect_listener["DefaultActions"][0]["RedirectConfig"]
    launch_template = tasks_by_module["amazon.aws.ec2_launch_template"][0]["amazon.aws.ec2_launch_template"]
    autoscaling_group = tasks_by_module["amazon.aws.autoscaling_group"][0]["amazon.aws.autoscaling_group"]
    scaling_policy = tasks_by_module["community.aws.autoscaling_policy"][0]["community.aws.autoscaling_policy"]["target_tracking_config"]
    subnet_group = tasks_by_module["amazon.aws.rds_subnet_group"][0]["amazon.aws.rds_subnet_group"]
    database_tasks = {task["amazon.aws.rds_instance"]["db_instance_identifier"]: task["amazon.aws.rds_instance"]
                      for task in tasks_by_module["amazon.aws.rds_instance"]}
    primary = database_tasks["renovation-primary"]
    replica = database_tasks["renovation-replica"]

    return {
        "security_groups": security_groups,
        "load_balancer": {
            "name": load_balancer["name"],
            "internet_facing": load_balancer["scheme"] == "internet-facing",
            "subnets": sorted(fill(load_balancer["subnets"])),
            "security_groups": sorted(fill(group) for group in load_balancer["security_groups"]),
        },
        "target_group": {
            "name": target_group["name"],
            "port": int(target_group["port"]),
            "protocol": target_group["protocol"],
            "health_check_path": target_group["health_check_path"],
        },
        "https_listener": {
            "port": int(https_listener["Port"]),
            "protocol": https_listener["Protocol"],
            "ssl_policy": https_listener["SslPolicy"],
            "certificate": fill(https_listener["Certificates"][0]["CertificateArn"]),
            "action": https_listener["DefaultActions"][0]["Type"],
        },
        "redirect_listener": {
            "port": int(redirect_listener["Port"]),
            "protocol": redirect_listener["Protocol"],
            "redirect_to": (str(redirect["Port"]), redirect["Protocol"], redirect["StatusCode"]),
        },
        "launch_template": {
            "image": fill(launch_template["image_id"]),
            "instance_type": launch_template["instance_type"],
            "security_groups": sorted(fill(group) for group in launch_template["security_group_ids"]),
            "metadata_tokens": launch_template.get("metadata_options", {}).get("http_tokens", "optional"),
        },
        "autoscaling_group": {
            "min": int(autoscaling_group["min_size"]),
            "max": int(autoscaling_group["max_size"]),
            "desired": int(autoscaling_group["desired_capacity"]),
            "subnets": sorted(fill(autoscaling_group["vpc_zone_identifier"])),
            "health_check_type": autoscaling_group.get("health_check_type", "EC2"),
            "health_check_grace_seconds": int(autoscaling_group.get("health_check_period", 300)),
        },
        "scaling_policy": {
            "metric": scaling_policy["predefined_metric_spec"]["predefined_metric_type"],
            "target": int(scaling_policy["target_value"]),
        },
        "database_subnets": sorted(fill(subnet_group["subnets"])),
        "primary_database": {
            "identifier": primary["db_instance_identifier"],
            "engine": primary["engine"],
            "engine_version": str(primary.get("engine_version", "unpinned")),
            "instance_class": primary["db_instance_class"],
            "storage": int(primary["allocated_storage"]),
            "database_name": primary["db_name"],
            "username": primary["master_username"],
            "password_from_outside": primary["master_user_password"] == "{{ database_password }}"
                                     and any(prompt["name"] == "database_password" and prompt.get("private")
                                             for prompt in playbook.get("vars_prompt", [])),
            "backup_days": int(primary["backup_retention_period"]),
            "encrypted": bool(primary["storage_encrypted"]),
            "security_groups": sorted(fill(group) for group in primary["vpc_security_group_ids"]),
        },
        "replica_database": {
            "identifier": replica["db_instance_identifier"],
            "source": replica["source_db_instance_identifier"] if replica.get("read_replica") else None,
            "instance_class": replica["db_instance_class"],
            "security_groups": sorted(fill(group) for group in replica["vpc_security_group_ids"]),
        },
    }


def read_cloudformation():
    import yaml

    class TemplateLoader(yaml.SafeLoader):
        pass

    def reference_tag(loader, node):
        return {"Ref": loader.construct_scalar(node)}

    def attribute_tag(loader, node):
        return {"GetAtt": loader.construct_scalar(node)}

    TemplateLoader.add_constructor("!Ref", reference_tag)
    TemplateLoader.add_constructor("!GetAtt", attribute_tag)
    template = yaml.load(CLOUDFORMATION_PATH.read_text(), Loader=TemplateLoader)
    resources = template["Resources"]

    def resource_name(value):
        if isinstance(value, dict) and "Ref" in value:
            return value["Ref"]
        if isinstance(value, dict) and "GetAtt" in value:
            return value["GetAtt"].split(".")[0]
        return value

    group_names = {}
    for logical_name, resource in resources.items():
        if resource["Type"] == "AWS::EC2::SecurityGroup":
            group_names[logical_name] = resource["Properties"]["GroupName"]

    def group_name(value):
        logical_name = resource_name(value)
        if isinstance(value, dict) and "GetAtt" in value and not value["GetAtt"].endswith(".GroupId"):
            return "WRONG ATTRIBUTE " + value["GetAtt"]
        if isinstance(value, dict) and "Ref" in value:
            return "REF RETURNS THE NAME, NOT THE ID: " + logical_name
        return group_names.get(logical_name, logical_name)

    security_groups = {}
    for resource in resources.values():
        if resource["Type"] != "AWS::EC2::SecurityGroup":
            continue
        properties = resource["Properties"]
        ingress_rules = []
        for rule in properties.get("SecurityGroupIngress", []):
            source = rule.get("CidrIp") or group_name(rule.get("SourceSecurityGroupId"))
            ingress_rules.append({"port": int(rule["FromPort"]), "source": source})
        open_egress = any(str(rule.get("IpProtocol")) == "-1" and rule.get("CidrIp") == "0.0.0.0/0"
                          for rule in properties.get("SecurityGroupEgress", []))
        security_groups[properties["GroupName"]] = {"ingress": security_group_rules(ingress_rules, {}),
                                                    "open_egress": open_egress}

    def of_type(type_name):
        return [resource["Properties"] for resource in resources.values() if resource["Type"] == type_name]

    load_balancer = of_type("AWS::ElasticLoadBalancingV2::LoadBalancer")[0]
    target_group = of_type("AWS::ElasticLoadBalancingV2::TargetGroup")[0]
    listeners = {listener["Port"]: listener for listener in of_type("AWS::ElasticLoadBalancingV2::Listener")}
    https_listener = listeners[443]
    redirect_listener = listeners[80]
    redirect = redirect_listener["DefaultActions"][0]["RedirectConfig"]
    launch_template = of_type("AWS::EC2::LaunchTemplate")[0]["LaunchTemplateData"]
    autoscaling_group = of_type("AWS::AutoScaling::AutoScalingGroup")[0]
    scaling_policy = of_type("AWS::AutoScaling::ScalingPolicy")[0]["TargetTrackingConfiguration"]
    subnet_group = of_type("AWS::RDS::DBSubnetGroup")[0]
    databases = {properties["DBInstanceIdentifier"]: properties for properties in of_type("AWS::RDS::DBInstance")}
    primary = databases["renovation-primary"]
    replica = databases["renovation-replica"]
    password_value = primary.get("MasterUserPassword")
    password_parameter = template.get("Parameters", {}).get(resource_name(password_value), {})

    return {
        "security_groups": security_groups,
        "load_balancer": {
            "name": load_balancer["Name"],
            "internet_facing": load_balancer["Scheme"] == "internet-facing",
            "subnets": sorted(load_balancer["Subnets"]),
            "security_groups": sorted(group_name(group) for group in load_balancer["SecurityGroups"]),
        },
        "target_group": {
            "name": target_group["Name"],
            "port": int(target_group["Port"]),
            "protocol": target_group["Protocol"],
            "health_check_path": target_group["HealthCheckPath"],
        },
        "https_listener": {
            "port": int(https_listener["Port"]),
            "protocol": https_listener["Protocol"],
            "ssl_policy": https_listener["SslPolicy"],
            "certificate": https_listener["Certificates"][0]["CertificateArn"],
            "action": https_listener["DefaultActions"][0]["Type"],
        },
        "redirect_listener": {
            "port": int(redirect_listener["Port"]),
            "protocol": redirect_listener["Protocol"],
            "redirect_to": (str(redirect["Port"]), redirect["Protocol"], redirect["StatusCode"]),
        },
        "launch_template": {
            "image": launch_template["ImageId"],
            "instance_type": launch_template["InstanceType"],
            "security_groups": sorted(group_name(group) for group in launch_template["SecurityGroupIds"]),
            "metadata_tokens": launch_template.get("MetadataOptions", {}).get("HttpTokens", "optional"),
        },
        "autoscaling_group": {
            "min": int(autoscaling_group["MinSize"]),
            "max": int(autoscaling_group["MaxSize"]),
            "desired": int(autoscaling_group["DesiredCapacity"]),
            "subnets": sorted(autoscaling_group["VPCZoneIdentifier"]),
            "health_check_type": autoscaling_group.get("HealthCheckType", "EC2"),
            "health_check_grace_seconds": int(autoscaling_group.get("HealthCheckGracePeriod", 0)),
        },
        "scaling_policy": {
            "metric": scaling_policy["PredefinedMetricSpecification"]["PredefinedMetricType"],
            "target": int(scaling_policy["TargetValue"]),
        },
        "database_subnets": sorted(subnet_group["SubnetIds"]),
        "primary_database": {
            "identifier": primary["DBInstanceIdentifier"],
            "engine": primary["Engine"],
            "engine_version": str(primary.get("EngineVersion", "unpinned")),
            "instance_class": primary["DBInstanceClass"],
            "storage": int(primary["AllocatedStorage"]),
            "database_name": primary["DBName"],
            "username": primary["MasterUsername"],
            "password_from_outside": bool(password_parameter.get("NoEcho")),
            "backup_days": int(primary["BackupRetentionPeriod"]),
            "encrypted": bool(primary["StorageEncrypted"]),
            "security_groups": sorted(group_name(group) for group in primary["VPCSecurityGroups"]),
        },
        "replica_database": {
            "identifier": replica["DBInstanceIdentifier"],
            "source": databases[resource_name_to_identifier(resources, replica["SourceDBInstanceIdentifier"])]["DBInstanceIdentifier"],
            "instance_class": replica["DBInstanceClass"],
            "security_groups": sorted(group_name(group) for group in replica["VPCSecurityGroups"]),
        },
    }


def resource_name_to_identifier(resources, value):
    """!Ref on a database returns its identifier, so follow the reference to the identifier it names."""
    if isinstance(value, dict) and "Ref" in value:
        return resources[value["Ref"]]["Properties"]["DBInstanceIdentifier"]
    return value


def compare(reference, other, other_label, path=""):
    if isinstance(reference, dict):
        for key in reference:
            if key not in other:
                report(False, other_label + " is missing " + path + key)
                continue
            compare(reference[key], other[key], other_label, path + key + ".")
        for key in other:
            if key not in reference:
                report(False, other_label + " has extra " + path + key)
        return
    if reference != other:
        report(False, other_label + " differs at " + path.rstrip("."),
               "Terraform has " + json.dumps(reference) + ", " + other_label + " has " + json.dumps(other))


def check_same_plan():
    try:
        terraform_plan = read_terraform()
        ansible_plan = read_ansible()
        cloudformation_plan = read_cloudformation()
    except ImportError as missing_module:
        skipped.append("same-plan comparison (" + str(missing_module) + ")")
        print("  skip same-plan comparison (" + str(missing_module) + ")")
        return
    failures_before = len(failures)
    compare(terraform_plan, ansible_plan, "Ansible")
    compare(terraform_plan, cloudformation_plan, "CloudFormation")
    for plan_label, plan in (("Terraform", terraform_plan), ("Ansible", ansible_plan), ("CloudFormation", cloudformation_plan)):
        public_subnets = set(plan["load_balancer"]["subnets"])
        private_tiers_clear = not public_subnets.intersection(plan["autoscaling_group"]["subnets"]) \
            and not public_subnets.intersection(plan["database_subnets"])
        report(private_tiers_clear, plan_label + ": API tier and database are outside the load balancer's public subnets")
        report(plan["launch_template"]["metadata_tokens"] == "required", plan_label + ": instances require IMDSv2")
        report(plan["autoscaling_group"]["health_check_type"] == "ELB", plan_label + ": unhealthy instances are replaced")
        report(plan["primary_database"]["engine_version"] != "unpinned", plan_label + ": database version is pinned")
    if len(failures) == failures_before:
        setting_count = count_settings(terraform_plan)
        report(True, "Ansible and CloudFormation match the Terraform", str(setting_count) + " settings compared")


def count_settings(plan):
    if isinstance(plan, dict):
        return sum(count_settings(value) for value in plan.values())
    return 1


def check_no_passwords():
    """Sai's note: the prompt said no credentials, and the first draft still had one."""
    for example_path in [TERRAFORM_PATH, ANSIBLE_PATH, CLOUDFORMATION_PATH]:
        file_text = example_path.read_text().lower()
        has_literal = ('"password"' in file_text or "password: password" in file_text
                       or "masteruserpassword: password" in file_text)
        report(not has_literal, "no literal password in " + example_path.relative_to(REPO_FOLDER).as_posix())


def main():
    print("Format checkers")
    check_terraform()
    check_ansible()
    check_cloudformation()
    check_protobuf()
    check_graphql()
    check_openapi()
    check_asyncapi()
    print("API server")
    check_api_server()
    print("Same plan in Terraform, Ansible, and CloudFormation")
    check_same_plan()
    check_no_passwords()
    if skipped:
        print("Skipped (not installed): " + "; ".join(skipped))
    if failures:
        print("FAILED (" + str(len(failures)) + ")")
        sys.exit(1)
    print("PASSED")


if __name__ == "__main__":
    main()

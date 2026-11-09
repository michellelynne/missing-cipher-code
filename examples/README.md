# Code examples

Working versions of the code in the book. Each one is checked on every push by the
[Code examples workflow](../.github/workflows/examples.yml), so what you copy here runs.

## Chapter 4: Renovation Revolution

The case study's contractor directory, built the ways Chapter 4 compares.

| Folder | What it holds |
|---|---|
| [`infrastructure-as-code/terraform/`](chapter-4/infrastructure-as-code/terraform/main.tf) | The plan from the chapter: a load balancer, an API tier, and a PostgreSQL database on AWS. |
| [`infrastructure-as-code/ansible/`](chapter-4/infrastructure-as-code/ansible/playbook.yml) | The same plan in Ansible. |
| [`infrastructure-as-code/cloudformation/`](chapter-4/infrastructure-as-code/cloudformation/template.yaml) | The same plan in CloudFormation. |
| [`api/`](chapter-4/api/) | The Contractors API in REST ([`openapi.yaml`](chapter-4/api/openapi.yaml)), gRPC ([`contractor.proto`](chapter-4/api/contractor.proto)), and GraphQL ([`schema.graphql`](chapter-4/api/schema.graphql)), with example requests and responses for each. |
| [`api/messaging/`](chapter-4/api/messaging/) | Polling, server-sent events, WebSockets, a queue and event bus, and signed webhooks, described in [AsyncAPI](chapter-4/api/messaging/asyncapi.yaml). |
| [`api/database/`](chapter-4/api/database/) | The PostgreSQL schema, seed data, and the queries the API runs. |
| [`api/server/`](chapter-4/api/server/) | One Python server that answers all three API styles from the same rules, plus a demo page. |

The three infrastructure files build the same thing. A check compares 50 settings across them
and fails if one drifts from the Terraform.

The example request and response files (`rest.http`, `graphql.http`, `grpc-calls.sh`, and the
`.http` files in `messaging/`) are real: the tests send every request to a fresh server and
compare the answers.

### Run the API

With Docker, which also starts PostgreSQL with the schema loaded:

```bash
cd examples/chapter-4/api
docker compose up                              # then open http://localhost:8000/demo
docker compose run --rm api python -m pytest   # every test, database ones included
```

Or with Python 3.11 or newer:

```bash
cd examples/chapter-4/api/server
python3 -m pip install -r requirements.txt
python3 -m pytest   # every example file, run against a fresh server
python3 app.py      # then open http://localhost:8000/demo
```

The server listens on port 8000 for REST, GraphQL, and the messaging examples, and on port 50051
for gRPC. Sign in with the demo tokens `homeowner-token`, `contractor-token`, or
`second-contractor-token`.

### Use the infrastructure files with care

These files create real AWS resources that cost money. Read them, change the names and region to
yours, and run `terraform plan` (or the Ansible or CloudFormation equivalent) before you apply
anything. Tear them down when you're done.

## Check your changes

```bash
npm ci
python3 -m pip install "python-hcl2>=7" ansible ansible-lint cfn-lint graphql-core openapi-spec-validator playwright
python3 -m pip install -r examples/chapter-4/api/server/requirements.txt
ansible-galaxy collection install -r examples/chapter-4/infrastructure-as-code/ansible/requirements.yml
python3 -m playwright install chromium
python3 tools/check_examples.py
```

Set `DATABASE_URL` to a PostgreSQL you can throw away to run the database tests too. Tools that
aren't installed are skipped and listed at the end, so you can run what you have.

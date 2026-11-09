# Case study reference: code and infrastructure

Renovation Revolution is the app the book's case study builds, for the homeowners, contractors,
and vendors on a renovation. This folder holds a working version of its backend and
infrastructure, so you can read, run, and change what the book describes. Everything here is checked on every push by the
[Case study reference workflow](../.github/workflows/examples.yml), so what you copy runs.

Download it all as [case-study-reference.zip](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/case-study-reference.zip),
or clone the repository.

## Infrastructure

The same plan in three tools: a load balancer that only takes HTTPS, two to six API instances
that scale on CPU, and a PostgreSQL database with a read replica. The API tier and the database
sit in private subnets, and only the load balancer faces the internet.

| File | Tool |
|---|---|
| [`infrastructure/terraform/main.tf`](infrastructure/terraform/main.tf) | Terraform, the version printed in the book |
| [`infrastructure/ansible/playbook.yml`](infrastructure/ansible/playbook.yml) | Ansible, with its collections in [`requirements.yml`](infrastructure/ansible/requirements.yml) |
| [`infrastructure/cloudformation/template.yaml`](infrastructure/cloudformation/template.yaml) | CloudFormation |

A check compares 50 settings across the three and fails if Ansible or CloudFormation drifts from
the Terraform.

These files create real AWS resources that cost money. Read them, change the names and region to
yours, and run `terraform plan` (or the Ansible or CloudFormation equivalent) before you apply
anything. Tear them down when you're done.

## Code

The Contractors Directory API, in each style the book compares, served by one Python server that
applies the same rules to all of them.

| Folder or file | What it holds |
|---|---|
| [`code/openapi.yaml`](code/openapi.yaml), [`code/rest.http`](code/rest.http) | REST: the OpenAPI description, and requests with their responses |
| [`code/contractor.proto`](code/contractor.proto), [`code/grpc-calls.sh`](code/grpc-calls.sh) | gRPC: the Protocol Buffers service, and grpcurl calls with their responses |
| [`code/schema.graphql`](code/schema.graphql), [`code/graphql.http`](code/graphql.http) | GraphQL: the schema, and queries and mutations with their responses |
| [`code/messaging/`](code/messaging/) | Polling, server-sent events, WebSockets, a queue and event bus, and signed webhooks, described in [AsyncAPI](code/messaging/asyncapi.yaml) |
| [`code/database/`](code/database/) | The PostgreSQL schema, seed data, and the queries the API runs |
| [`code/server/`](code/server/) | The server, its tests, and a demo page |

The request and response files are real: the tests send every request to a fresh server and
compare the answers.

### Run it

With Docker, which also starts PostgreSQL with the schema loaded:

```bash
cd case-study-reference/code
docker compose up                              # then open http://localhost:8000/demo
docker compose run --rm api python -m pytest   # every test, database ones included
```

Or with Python 3.11 or newer:

```bash
cd case-study-reference/code/server
python3 -m pip install -r requirements.txt
python3 -m pytest   # every example file, run against a fresh server
python3 app.py      # then open http://localhost:8000/demo
```

The server listens on port 8000 for REST, GraphQL, and the messaging examples, and on port 50051
for gRPC. Sign in with the demo tokens `homeowner-token`, `contractor-token`, or
`second-contractor-token`.

## Check your changes

```bash
npm ci
python3 -m pip install "python-hcl2>=7" ansible ansible-lint cfn-lint graphql-core openapi-spec-validator playwright
python3 -m pip install -r case-study-reference/code/server/requirements.txt
ansible-galaxy collection install -r case-study-reference/infrastructure/ansible/requirements.yml
python3 -m playwright install chromium
python3 tools/check_examples.py
```

Set `DATABASE_URL` to a PostgreSQL you can throw away to run the database tests too. Tools that
aren't installed are skipped and listed at the end, so you can run what you have.

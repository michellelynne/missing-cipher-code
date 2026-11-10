# Case study reference: code and infrastructure

Renovation Revolution is the app the book's case study builds, for the homeowners, contractors,
and vendors on a renovation. This folder holds a working version of its backend and
infrastructure, so you can read, run, and change what the book describes. Everything here is checked on every push by the
[Case study reference workflow](../.github/workflows/examples.yml), so what you copy runs. The
server's container image is built, scanned, tested, and (on main) signed and published by the
[Container image workflow](../.github/workflows/container.yml).

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
| [`code/Dockerfile`](code/Dockerfile), [`code/compose.yaml`](code/compose.yaml) | The server's container image, and Compose to run it with PostgreSQL |
| [`code/compose.published.yaml`](code/compose.published.yaml), [`code/ops/update.py`](code/ops/update.py) | Run the signed, published image by digest, and update or roll it back |

The request and response files are real: the tests send every request to a fresh server and
compare the answers.

### Run it

With Docker, which also starts PostgreSQL with the schema loaded:

```bash
cd case-study-reference/code
docker compose up                # then open http://localhost:8000/demo
docker compose run --rm tests    # every test, database ones included, in the test image
```

The image that runs has no shell and no package manager, runs as a regular user, and Compose
starts it with a read-only filesystem. The tests run in a separate test image built from the same
base. [DESIGN.md](../DESIGN.md#the-case-studys-container-image) explains the choices.

Or with Python 3.11 or newer:

```bash
cd case-study-reference/code/server
python3 -m pip install -r requirements-test.txt
python3 -m pytest   # every example file, run against a fresh server
python3 app.py      # then open http://localhost:8000/demo
```

`requirements.txt` is what the running server needs, and it's all the image installs.
`requirements-test.txt` adds the tests' libraries and grpcio-tools, which turns `contractor.proto`
into Python when the server starts. The image does that while it builds instead.

### Run the signed image

Every push to main publishes the image to
`ghcr.io/michellelynne/renovation-revolution`, after it passes its tests and a vulnerability scan.
The [Container image workflow](../.github/workflows/container.yml) signs it with
[Cosign](https://docs.sigstore.dev/cosign/) and attaches a signed SBOM (the list of every package
inside) and GitHub's build provenance (which workflow and commit built it). There's no signing key:
the signature is tied to that workflow on main, and recorded in Sigstore's public transparency log.

Run it by digest (`@sha256:...`), never by tag. A tag can be moved to point at different bytes; a
digest can't, so what you verified is what runs. With [cosign](https://docs.sigstore.dev/cosign/system_config/installation/)
installed, from `case-study-reference/code`:

```bash
# 1. Find the newest signed image (this checks its signature too)
python3 ops/update.py --verify-only
export RENOVATION_IMAGE=ghcr.io/michellelynne/renovation-revolution@sha256:<the digest it printed>

# 2. Check the signature yourself. It fails unless this repository's workflow, on main, signed it.
cosign verify "$RENOVATION_IMAGE" \
  --certificate-identity https://github.com/michellelynne/missing-cipher-code/.github/workflows/container.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com

# 3. Run it, with the same PostgreSQL as compose.yaml
docker compose -f compose.published.yaml up -d
```

To see what's in the image, verify the SBOM attestation and print its packages:

```bash
cosign verify-attestation "$RENOVATION_IMAGE" --type spdxjson \
  --certificate-identity https://github.com/michellelynne/missing-cipher-code/.github/workflows/container.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  | jq -r '.payload' | head -n 1 | base64 -d | jq -r '.predicate.packages[] | .name + " " + .versionInfo'
```

To check the build provenance with the GitHub CLI:
`gh attestation verify "oci://$RENOVATION_IMAGE" --repo michellelynne/missing-cipher-code`.
Each workflow run also keeps the SBOM and the full Trivy report as a download.

To pin a version, keep `RENOVATION_IMAGE` set to that digest; the image never changes under you.
Every image is also tagged with its commit (`sha-<commit>`) and the time it was built
(`2026-11-10.153012`), so you can find the digest for a given commit.

### Update and roll back

[`ops/update.py`](code/ops/update.py) moves a running copy of `compose.published.yaml` to a new
image safely. It needs Python, Docker Compose, and cosign, and no registry password, since the
image is public.

```bash
python3 ops/update.py                          # the newest signed image
python3 ops/update.py --digest sha256:<digest> # one exact image: pin, or roll back by hand
```

It finds the newest dated tag, checks the signature of its digest and refuses an unsigned image
(trying the next newest instead), notes the digest that's running, starts the new one, and waits
for its health check (`GET /health`). If the new image doesn't become healthy, it starts the
previous digest again. Each change is added to `ops/deploy-history.log`. If you sign with your own
key instead, pass `--key cosign.pub`.

The server listens on port 8000 for REST, GraphQL, and the messaging examples, and on port 50051
for gRPC. Sign in with the demo tokens `homeowner-token`, `contractor-token`, or
`second-contractor-token`.

## Check your changes

```bash
npm ci
python3 -m pip install "python-hcl2>=7" ansible ansible-lint cfn-lint graphql-core openapi-spec-validator playwright
python3 -m pip install -r case-study-reference/code/server/requirements-test.txt
ansible-galaxy collection install -r case-study-reference/infrastructure/ansible/requirements.yml
python3 -m playwright install chromium
python3 tools/check_examples.py
```

Set `DATABASE_URL` to a PostgreSQL you can throw away to run the database tests too. Tools that
aren't installed are skipped and listed at the end, so you can run what you have.

## License

The code and infrastructure here are under the [MIT License](LICENSE), so you can use them in your
own projects, including at work. Please keep the copyright notice and credit:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

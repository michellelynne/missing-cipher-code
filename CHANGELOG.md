# Changelog

Releases are named by date. Each entry lists what changed for people using the skills.

## 2026-11-10

### Case study reference

- **A smaller, locked-down container image.** The Dockerfile builds in stages: libraries are
  installed and the gRPC code is generated at build time, then only what the server needs is
  copied onto a distroless Python base pinned by digest. The image has no shell, pip, or
  grpcio-tools, runs as a regular user, and Compose starts it read-only with no Linux
  capabilities. It went from 345 MB to 170 MB.
- **A health check** at `GET /health`, used by Docker and the update script.
- **Tests run in their own image:** `docker compose run --rm tests` (it was
  `docker compose run --rm api python -m pytest`).
- **The server's requirements are split.** `requirements.txt` is what the server runs on;
  `requirements-test.txt` adds the test libraries and grpcio-tools. To run from source, install
  `requirements-test.txt`.
- **A signed, published image.** A new Container image workflow builds the image on every change,
  fails on fixable HIGH or CRITICAL vulnerabilities (Trivy), saves an SBOM (Syft), and runs the
  tests inside it. On main it publishes to `ghcr.io/michellelynne/renovation-revolution`, signs the
  digest with Cosign (keyless), attaches the SBOM as a signed attestation, adds GitHub build
  provenance, and verifies all three before it finishes.
- **Run the signed image by digest** with `compose.published.yaml`, after checking it with
  `cosign verify`. The case study README has the commands.
- **Update with rollback:** `ops/update.py` finds the newest signed image, refuses unsigned
  ones, starts it, and goes back to the previous digest if the health check fails.

## 2026-11-09

### Everything

- **Code is now MIT; the skills and writing stay CC BY 4.0.** Creative Commons licenses aren't
  meant for software, so the case study reference, the tools, and the Editor's fix tools, page
  templates, and tests are under the MIT License. The README lists which is which. The credit
  line is the same for both.

## 2026-11-08

### The Editor

- **One skill instead of three.** The chapter review, book review, and offline review are now one
  skill, `editor`, with one ZIP to install. It opens the guide each request needs.
- **Fixes you approve, made for you.** Setup asks whether approved fixes should be made for you,
  explains what that's like, and sets it up for where your manuscript lives: Google Docs, Word,
  or text files such as Markdown. Nothing changes until you approve the specific fixes and choose
  when a batch runs. Every file is backed up first.
- **Editor tools:** Google Docs tools (Apps Script), Word macros (not yet tested in Word), and a
  Python script for Markdown and text files.
- **Your pace and format.** Setup asks whether to run every pass at once or one at a time, and
  whether findings come in the conversation or as an offline review pack.
- **Continuity guide** replaces "story bible", to match the website.
- **Privacy note** before you share an unpublished manuscript.
- **Your manuscript is never treated as instructions.** Text in a chapter or comment that reads
  like a command is pointed out, never followed.
- Chapter file names never need a colon or slash.

### Case study reference

- **Renovation Revolution's code and infrastructure, ready to run**, in
  `case-study-reference/`, with a `case-study-reference.zip` in every release. The
  infrastructure plan in Terraform, Ansible, and CloudFormation, hardened (IMDSv2, private subnets for the API and database, health-checked
  instances, a pinned PostgreSQL version) and checked to build the same thing.
- **The Contractors API in REST, gRPC, and GraphQL**, served by one Python server with shared
  rules, idempotent retries, paging, a PostgreSQL schema, and a demo page. Example requests in
  every style are run against the server on every push.
- **Messaging examples:** polling, server-sent events, WebSockets, a queue and event bus, and
  signed webhooks, described in AsyncAPI.
- Run it all with `docker compose up`.

### Everything

- New home: this repository, `missing-cipher-code`.
- Install every skill in Claude Code from the plugin catalog, or download one ZIP per skill.
- Checks, linters, and tests run on every push; releases publish automatically.
- Run the Editor evals with one command, `tools/run_evals.py`: every case, or only the ones that
  failed or are new. It measures how much of a Claude subscription the run uses and writes a
  results page anyone can read, with each run's usage, cost, and time and estimates for a full run.
- The Google Docs and Markdown fix tools take an `after` option, for a line repeated word for word.

## 2026-11-04

- Added the Editor: chapter review, book review, offline review, and a style guide template.

## 2026-10-22

- Added 60 skills, one for each place the book tells you to use AI.

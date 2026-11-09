# Changelog

Releases are named by date. Each entry lists what changed for people using the skills.

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

## 2026-11-04

- Added the Editor: chapter review, book review, offline review, and a style guide template.

## 2026-10-22

- Added 60 skills, one for each place the book tells you to use AI.

# The Missing Cipher: code and AI skills

[![Tests](https://github.com/michellelynne/missing-cipher-code/actions/workflows/tests.yml/badge.svg)](https://github.com/michellelynne/missing-cipher-code/actions/workflows/tests.yml)
[![Code examples](https://github.com/michellelynne/missing-cipher-code/actions/workflows/examples.yml/badge.svg)](https://github.com/michellelynne/missing-cipher-code/actions/workflows/examples.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

Companion code for *The Missing Cipher: The Field Guide for Senior Software Engineers* by
Michelle Brenner (Packt). Everything here is free to use under [CC BY 4.0](LICENSE).

| Folder | What it holds |
|---|---|
| [`skills/`](skills/) | 60 AI skills, one for each place the book tells you to use AI. Start with the [skills index](skills/README.md). |
| [`skills/editor/`](skills/editor/) | The Editor: an AI skill that reviews any book manuscript, chapter by chapter or across the whole book, with fixes you approve. |
| [`examples/`](examples/) | Working code from the book: Chapter 4's infrastructure in Terraform, Ansible, and CloudFormation, and its API in REST, gRPC, and GraphQL with a server you can run. Start with the [examples index](examples/README.md). |
| [`tools/`](tools/) | Scripts that check the skills and the code examples, build the plugin catalog and release ZIPs, and report eval cost and speed. |

## Installing the skills

Each skill is a folder with a `SKILL.md` file, in the open skills format that Claude and other AI
tools support.

**Download a ZIP** for chat apps that take a skill upload. Each link is always the newest release:

- [The Editor](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/editor.zip)
- [Every skill](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/all-skills.zip)
- One skill: `https://github.com/michellelynne/missing-cipher-code/releases/latest/download/<skill-name>.zip`

**In Claude Code**, add this repository as a plugin marketplace and install either plugin:

```text
/plugin marketplace add michellelynne/missing-cipher-code
/plugin install book-editor@missing-cipher
/plugin install missing-cipher-skills@missing-cipher
```

Or copy a skill folder into `~/.claude/skills/`:

```bash
cp -r skills/job-alert-query-builder ~/.claude/skills/
```

Every skill also includes a prompt you can paste into any AI chat, so you can use it without
installing anything.

## How it's built and tested

- [DESIGN.md](DESIGN.md) explains the decisions: why fixes are exact search strings, why the
  author approves every change, which places a manuscript can live, and why manuscript text is
  treated as untrusted input.
- Every push runs the [Tests workflow](.github/workflows/tests.yml): skill checks, the plugin
  catalog, linters, and the editor tool tests.
- Every change to the code examples runs the [Code examples workflow](.github/workflows/examples.yml):
  real Terraform, Ansible, and CloudFormation linters, the API server's tests against PostgreSQL
  and a browser, and a Docker build.
- The Editor's model evals compare runs with and without the skill. See
  [How it's tested](skills/editor/README.md#how-its-tested).
- Releases are named by date and published automatically. See [CHANGELOG.md](CHANGELOG.md).

## A note on AI

Treat everything these skills produce as a first draft. Verify anything the AI could not source,
never paste secrets or proprietary code into a public model, and review the work before you use it.

## License and credit

Licensed under [CC BY 4.0](LICENSE). Please credit:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). Learn more about the book at
[themissingcipher.com](https://themissingcipher.com/).

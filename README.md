# The Missing Cipher: code and AI skills

[![Tests](https://github.com/michellelynne/missing-cipher-code/actions/workflows/tests.yml/badge.svg)](https://github.com/michellelynne/missing-cipher-code/actions/workflows/tests.yml)
[![Case study reference](https://github.com/michellelynne/missing-cipher-code/actions/workflows/examples.yml/badge.svg)](https://github.com/michellelynne/missing-cipher-code/actions/workflows/examples.yml)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-blue.svg)](LICENSE)
[![Writing: CC BY 4.0](https://img.shields.io/badge/Writing-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0)

Companion code for *The Missing Cipher: The Field Guide for Senior Software Engineers* by
Michelle Brenner (Packt): 60 AI skills for engineers, the Editor, an AI skill that reviews any
book manuscript, and working code and infrastructure for the book's case study. Everything is
free to use: the code under [MIT](LICENSE) and the skills and writing under
[CC BY 4.0](LICENSE-CC-BY-4.0). See [License and credit](#license-and-credit).

- [What I built](#what-i-built)
- [How to use it](#how-to-use-it): install the skills, use the Editor, run the case study, run the evals, run the checks
- [What's in this repository](#whats-in-this-repository)

## What I built

### 60 AI skills, one for each place the book says to use AI

Each skill turns a recommendation from the book (draft a proposal memo, triage an alert, review
production readiness, write success statements for a promotion case) into instructions an AI
assistant can follow, with the book's cautions built in. They use the open skills format, so
they work in Claude and in other AI tools that support skills. Every skill also ends with a
prompt you can paste into any AI chat.

### The Editor: an AI book editor that only changes what you approve

I built the Editor while editing my own book and made it work for any book, fiction or
nonfiction. It reviews a chapter in passes (prose and style guide, house style, editorial flags
such as facts, structure, print risk and accessibility, then deliverables such as endnotes), or
the whole manuscript for problems that only show across chapters. Every finding comes with a
search string and a fix.

What makes it more than a prompt:

- **One skill, routed.** A short `SKILL.md` holds the rules every review shares and opens only
  the guide the request needs (chapter review, book review, or offline review pack), so long
  instructions load only when they're used.
- **The author approves every change.** Fixes are exact search strings that must match the
  current chapter exactly once. Nothing changes until the author approves specific fixes and
  chooses when a batch runs; every file is backed up first.
- **Fix tools for where manuscripts actually live:**
  - **Google Docs:** an Apps Script engine that checks, previews, and applies a batch, changes
    only the characters that differ so formatting survives, stops before Google's six-minute
    limit, and reports every fix as applied, already applied, or left for a hand fix.
  - **Word:** the assistant edits a copy with tracked changes, with Word macros as a fallback.
  - **Markdown and text files:** a Python script with the same check, preview, and apply steps.
- **Treats the manuscript as untrusted input.** Text in a chapter or comment that reads like an
  instruction to the AI ("ignore the style guide", "delete the backups folder") is reviewed and
  pointed out, never followed.
- **An offline review pack:** HTML pages that work with no internet, where the author marks each
  finding Fix, Skip, or Done and sends the marks back to be applied.

The decisions behind it, and what each one gave up, are in [DESIGN.md](DESIGN.md).

### Case study reference: code and infrastructure

Renovation Revolution, the app the book's case study builds, as working code:

- **The same infrastructure in Terraform, Ansible, and CloudFormation**, hardened (IMDSv2, private
  subnets for the API and database, health-checked instances, a pinned PostgreSQL version). A
  check compares 50 settings across the three and fails if one drifts.
- **The Contractors Directory API in REST, gRPC, and GraphQL**, served by one Python server with
  shared rules, idempotent retries, paging, and a PostgreSQL schema. Every example request in the
  repository is sent to a fresh server on every push, and the answers must match.
- **Messaging:** polling, server-sent events, WebSockets, a queue and event bus, and signed
  webhooks, described in AsyncAPI.

### Evals that measure what the Editor adds

The Editor is tested the way you'd test any software whose output isn't the same twice:

- **12 test cases with problems planted on purpose**, so every check has a known right answer:
  an em dash, an acronym never spelled out, a broken endnote sequence, a continuity slip in a
  novel, an instruction hidden in a chapter. Some cases check for false alarms instead, such as a
  clean chapter that should get a short report.
- **Every case runs with and without the skill**, so the results show what the skill adds rather
  than what the model already does. Across all 12 cases (the latest result of each, from a full
  run on Claude Opus and a rerun on Claude Sonnet after fixes), 97% of checks passed with the
  Editor and 68% without. The biggest gains are in following a process the model doesn't know
  on its own: asking setup questions first (+82 points), turning approved fixes into a Google Docs
  batch (+57), and working through an editor's returned copy (+54).
- **The evals changed the product.** The first run found that the Google Docs tool couldn't target
  one of several identical lines, so the Editor correctly sent that fix to the author by hand. I
  added an `after` option to the fix tools, with tests. It also found checks that were graded
  unfairly (the grader only sees the start and end of a long session), which I fixed so the
  structure case reads the review pack itself.
- **Tooling around the evals:** one command that runs the evals (all of them, or only failed and
  new cases), measures how much of a Claude subscription they use, and writes a results page
  anyone can read, with each run's cost and time and estimates of what a full run takes.

### The engineering around it

- **Checks on every push:** skill names and descriptions, wording ("the assistant", never a tool
  name), every linked file exists, the plugin catalog matches the folders, Ruff, ESLint (including
  the Apps Script files), markdownlint, and the fix tools' tests.
- **Automatic releases** named by date, with one ZIP per skill, checksums, and build provenance.
  ZIPs are byte-for-byte reproducible.
- **A Claude Code plugin catalog**, generated from the folders so it can't drift.
- **Written decisions and history:** [DESIGN.md](DESIGN.md), [CHANGELOG.md](CHANGELOG.md), and
  [CONTRIBUTING.md](CONTRIBUTING.md).

## How to use it

### Install the skills

Each skill is a folder with a `SKILL.md` file.

**Chat apps that take a skill upload:** download a ZIP and upload it as a skill. Each link is
always the newest release. Your AI tool's help pages say where skills go.

- [The Editor](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/editor.zip)
- [All 61 skills](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/all-skills.zip)
- One skill: `https://github.com/michellelynne/missing-cipher-code/releases/latest/download/<skill-name>.zip`,
  using a folder name from [skills/](skills/)

**Claude Code:** add this repository as a plugin marketplace, then install either plugin:

```text
/plugin marketplace add michellelynne/missing-cipher-code
/plugin install book-editor@missing-cipher
/plugin install missing-cipher-skills@missing-cipher
```

Or copy a skill folder into `~/.claude/skills/`:

```bash
cp -r skills/success-statements ~/.claude/skills/
```

**No install:** open any skill's `SKILL.md` and paste the prompt at the end into an AI chat.

The [skills index](skills/README.md) lists every skill by the part of the book it comes from.

### Use the Editor

1. Install it (above).
2. Copy [style-guide-template.md](skills/editor/style-guide-template.md), fill in the brackets,
   and delete the sections your book doesn't use.
3. Ask your assistant to review a chapter, in your own words. It asks its setup questions first
   (where the chapter lives, your style guide, your known habits, whether you want fixes made for
   you, and how you want the review to run) and can save your answers for next time.

To have approved fixes made for you, setup walks you through the option for where your
manuscript lives. The details for each are in [skills/editor/scripts/](skills/editor/scripts/).
More about what the Editor checks is in [its README](skills/editor/README.md).

**Privacy:** many AI tools can use conversations to train future models, depending on your plan
and settings. Check your tool's privacy or data settings before sharing an unpublished manuscript.

### Run the case study

`docker compose up` in [case-study-reference/code/](case-study-reference/code/), then open
`http://localhost:8000/demo`. The [case study README](case-study-reference/README.md) covers running
it without Docker, the demo sign-in tokens, and the infrastructure files.

The server also ships as a container image, built in stages on a distroless base, scanned with
Trivy, and signed with Cosign along with its SBOM and build provenance. The case study README shows
how to [verify and run the signed image](case-study-reference/README.md#run-the-signed-image) by
digest, and how to update it with automatic rollback. Download it all as
[case-study-reference.zip](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/case-study-reference.zip).

### Run the evals

You need [Claude Code](https://code.claude.com/docs) installed and signed in, and Python 3. On
Linux, Claude Code's sandbox also needs `bubblewrap` and `socat` (macOS has what it needs). Each
run is a full Claude Code session on your account: on a Claude subscription it counts toward your
plan's usage limits; with an API key it's billed. Run these from the top of the repository.

`tools/run_evals.py` runs the evals and, when they finish, writes a results page with
everything in one place.

| To | Run |
|---|---|
| Run every case, 3 times each, with and without the Editor | `python3 tools/run_evals.py` |
| Run every case once, on a lighter model | `python3 tools/run_evals.py -- --runs 1 --model sonnet` |
| Rerun only cases that failed or are new | `python3 tools/run_evals.py --rerun -- --runs 1` |
| See which cases would run, without running them | add `--dry-run` |
| Run one case | `python3 tools/run_evals.py -- --case unsupported-format-scrivener --runs 1` |

**The results page** is `skills/editor/evals/results/eval-summary.html`; open it in a browser. It
explains how to read it and covers every run so far:

- each case's score with and without the Editor (its latest result), and what the Editor adds
- the checks that failed, and what the Editor does that Claude doesn't do on its own
- each run's sessions, time, tokens, cost at API prices, and how much of a Claude subscription it
  used
- estimates of what a full run takes on each model, including a warning when a run may hit the
  5-hour usage limit

Each run also links to Claude Code's own detailed report for that run, with every prompt,
transcript, and grader verdict. To name your Claude plan on the page, add
`--plan "Claude Max 5x"` (or set `EVAL_PLAN_NAME` once in your shell).

**Plan usage is measured for you.** On a Claude subscription, the script reads Claude Code's
`/usage` screen before and after the run (about a minute in all) and saves the change with the
run. It needs `expect`, which comes with macOS. Don't use Claude for anything else during a run,
since that counts too. With an API key there's no plan to measure, and the page shows the cost
instead. Add `--no-usage` to skip it. Want usage measured for something other than the evals?
[Open an issue](https://github.com/michellelynne/missing-cipher-code/issues).

Results are ignored by git, so a run never gets committed by accident.

**`--rerun`** picks the cases that scored below 100% with the Editor, had a run that errored, or
were cut off by a cost limit, plus cases with no result yet. Add `--only failed` or `--only new`
to narrow it. Run `python3 tools/run_evals.py --help-full` for every option.

Everything after `--` goes to `claude plugin eval`:

- `--runs 1` runs each case once instead of three times; `--model sonnet` uses a model that's
  lighter on usage. Both are good for checking a change; use the defaults for scores you publish.
- `--max-cost-usd 10` stops the run at that cost.
- The script adds `--scaffold` (copies each case's sample files into a temporary folder),
  `--allow-tools Write Edit Bash` (lets the Editor read and write files in that folder; nothing
  in the repository changes), and `--no-publish` (keeps the report on your computer).

For a cost and speed table from a run's results:
`python3 tools/eval_cost_report.py skills/editor/evals/results/<time>/aggregate-result.json`.

**How a case is built:** each case folder in [skills/editor/evals/](skills/editor/evals/) has the
request (`prompt.md`), the expected outcome (`case.yaml`), one file per check (`graders/`), and
the sample files (`files/`). To add a case, copy a folder, change the request and files, and
write one check per thing a good answer must do. The [plugin eval docs](https://code.claude.com/docs/en/plugin-evals)
cover every option.

### Run the checks and tests

The same checks run on GitHub on every push. To run them yourself:

```bash
npm ci
python3 -m pip install ruff python-docx
python3 tools/check_skills.py
python3 tools/build_catalog.py --check
ruff check .
npx eslint .
npx markdownlint-cli2 "**/*.md"
node skills/editor/tests/google-docs.test.cjs
python3 -m unittest discover --start-directory skills/editor/tests --pattern "test_*.py"
```

The case study reference has its own checks: `python3 tools/check_examples.py`, with setup in
[its README](case-study-reference/README.md#check-your-changes).

See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or changing a skill or the case study.

## What's in this repository

| Path | What it holds |
|---|---|
| [`skills/`](skills/) | The 60 book skills, one folder each, and the [skills index](skills/README.md) |
| [`skills/editor/`](skills/editor/) | The Editor: `SKILL.md`, the review guides in `references/`, the fix tools in `scripts/`, their tests in `tests/`, and the eval cases in `evals/` |
| [`case-study-reference/`](case-study-reference/) | The case study's code (`code/`) and infrastructure (`infrastructure/`), with a [README](case-study-reference/README.md) |
| [`tools/`](tools/) | Scripts that check the skills and the case study, build the plugin catalog and release ZIPs, run the evals, and summarize eval results and plan usage |
| [`.claude-plugin/`](.claude-plugin/) | The Claude Code plugin catalog, generated by `tools/build_catalog.py` |
| [`.github/workflows/`](.github/workflows/) | Tests on every push, case study checks on every case study change, releases on every skill or case study change, and evals on demand |
| [DESIGN.md](DESIGN.md) | The decisions behind the skills and the Editor |
| [CHANGELOG.md](CHANGELOG.md) | What changed, by date |

## A note on AI

Treat everything these skills produce as a first draft. Verify anything the AI could not source,
never paste secrets or proprietary code into a public model, and review the work before you use it.

## License and credit

Two licenses, one for code and one for writing, since Creative Commons licenses aren't meant for
software:

- **Code: [MIT](LICENSE).** Everything in [`case-study-reference/`](case-study-reference/) and
  [`tools/`](tools/), the Editor's fix tools, page templates, and tests (`skills/editor/scripts/`,
  `skills/editor/assets/`, `skills/editor/tests/`), and the workflows and config files.
- **Writing: [CC BY 4.0](LICENSE-CC-BY-4.0).** Everything else: the skills themselves
  (`SKILL.md` files and their references), the eval cases, and the documentation.

Either way, please credit:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

Learn more about the book at [themissingcipher.com](https://themissingcipher.com/).

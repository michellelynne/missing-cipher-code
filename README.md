# The Missing Cipher: code and AI skills

[![Tests](https://github.com/michellelynne/missing-cipher-code/actions/workflows/tests.yml/badge.svg)](https://github.com/michellelynne/missing-cipher-code/actions/workflows/tests.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)

Companion code for *The Missing Cipher: The Field Guide for Senior Software Engineers* by
Michelle Brenner (Packt): 60 AI skills for engineers, plus the Editor, an AI skill that reviews
any book manuscript. Everything is free to use under [CC BY 4.0](LICENSE).

- [What I built](#what-i-built)
- [How to use it](#how-to-use-it): install the skills, use the Editor, run the evals, run the checks
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

### Evals that measure what the Editor adds

The Editor is tested the way you'd test any software whose output isn't the same twice:

- **12 test cases with problems planted on purpose**, so every check has a known right answer:
  an em dash, an acronym never spelled out, a broken endnote sequence, a continuity slip in a
  novel, an instruction hidden in a chapter. Some cases check for false alarms instead, such as a
  clean chapter that should get a short report.
- **Every case runs with and without the skill**, so the results show what the skill adds rather
  than what the model already does. In the first full run (Claude Opus, 8 cases, 3 runs each),
  89% of checks passed with the Editor and 70% without. The biggest gains were in following a
  process the model doesn't know on its own: asking setup questions first (+61 points) and working
  through an editor's returned copy (+44).
- **The evals changed the product.** That run found that the Google Docs tool couldn't target
  one of several identical lines, so the Editor correctly sent that fix to the author by hand. I
  added an `after` option to the fix tools, with tests. It also found checks that were graded
  unfairly (the grader only sees the start and end of a long session), which I fixed so the
  structure case reads the review pack itself.
- **Tooling around the evals:** a readable results page for anyone, a command that reruns only
  failed and new cases, a cost and speed table, and a wrapper that measures how much of a Claude
  subscription a run uses.

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

### Run the evals

You need [Claude Code](https://code.claude.com/docs) installed and signed in. Each run is a full
Claude Code session on your account: on a Claude subscription it counts toward your plan's usage
limits; with an API key it's billed. Run these from the top of the repository.

| To | Run |
|---|---|
| Try one case, cheaply | `claude plugin eval skills/editor --case unsupported-format-scrivener --runs 1 --model sonnet --scaffold --allow-tools Write Edit Bash --no-publish` |
| Run every case, 3 times each, with and without the Editor | `claude plugin eval skills/editor --scaffold --allow-tools Write Edit Bash --no-publish` |
| Rerun only cases that failed or are new | `python3 tools/rerun_evals.py -- --runs 1 --model sonnet` (add `--dry-run` to see the list first) |
| Make a readable results page | `python3 tools/eval_summary.py skills/editor/evals/results/*/aggregate-result.json` |
| Make a cost and speed table | `python3 tools/eval_cost_report.py skills/editor/evals/results/<run>/aggregate-result.json` |
| See how much of your Claude plan a run uses | `tools/measure_plan_usage.sh "label" <any command above>` |

What the eval options do:

- `--scaffold` copies each case's sample files into a temporary folder for the run.
- `--allow-tools Write Edit Bash` lets the Editor read and write files in that folder. Nothing in
  the repository changes.
- `--runs 1` runs each case once instead of three times; `--model sonnet` uses a model that's
  lighter on usage. Both are good for checking a change; use the defaults for scores you publish.
- `--no-publish` keeps the report on your computer.

Results and Claude Code's detailed report go to `skills/editor/evals/results/<time>/`. Results
are ignored by git, so a run never gets committed by accident.

**Measuring plan usage** (`tools/measure_plan_usage.sh`, macOS or Linux, needs `expect`) reads
Claude Code's `/usage` screen before and after the command and adds a line to
`skills/editor/evals/results/plan-usage.csv`. Don't use Claude for anything else while it runs,
since that counts too.

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

See [CONTRIBUTING.md](CONTRIBUTING.md) before adding or changing a skill.

## What's in this repository

| Path | What it holds |
|---|---|
| [`skills/`](skills/) | The 60 book skills, one folder each, and the [skills index](skills/README.md) |
| [`skills/editor/`](skills/editor/) | The Editor: `SKILL.md`, the review guides in `references/`, the fix tools in `scripts/`, their tests in `tests/`, and the eval cases in `evals/` |
| [`tools/`](tools/) | Scripts that check the skills, build the plugin catalog and release ZIPs, rerun evals, and summarize eval results and plan usage |
| [`.claude-plugin/`](.claude-plugin/) | The Claude Code plugin catalog, generated by `tools/build_catalog.py` |
| [`.github/workflows/`](.github/workflows/) | Tests on every push, releases on every skill change, and evals on demand |
| [DESIGN.md](DESIGN.md) | The decisions behind the skills and the Editor |
| [CHANGELOG.md](CHANGELOG.md) | What changed, by date |

## A note on AI

Treat everything these skills produce as a first draft. Verify anything the AI could not source,
never paste secrets or proprietary code into a public model, and review the work before you use it.

## License and credit

Licensed under [CC BY 4.0](LICENSE). Please credit:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

Learn more about the book at [themissingcipher.com](https://themissingcipher.com/).

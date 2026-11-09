# The Editor

One AI skill that reviews a book manuscript the way a careful editor would. It grew out of
editing *The Missing Cipher* and works for any book, fiction or nonfiction.

| File | What it does |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill itself. It reads the request and opens the guide the task needs. |
| [`references/chapter-review.md`](references/chapter-review.md) | Reviews one chapter in passes: style guide and prose habits, house style and figures, editorial flags (facts, structure, voice, print risk, accessibility), and deliverables such as endnotes and the chapter title. Every finding comes with a search string and a fix. |
| [`references/book-review.md`](references/book-review.md) | Checks what only shows across the whole manuscript: repeated stories and phrases, cross-references between chapters, first use of terms, chapter format drift, transitions, and the running example or continuity guide. |
| [`references/offline-review.md`](references/offline-review.md) | Turns the findings from either review into an offline review pack: HTML pages you can open with no internet to mark each finding Fix, Skip, or Done and export your marks. Send the marks back and it applies the Fix items. The page templates are in [`assets/`](assets/). |
| [`scripts/`](scripts/) | Editor tools that make the fixes you approve: an Apps Script project for Google Docs (plus word counts and images), Word macros that make each fix as a tracked change, and a Python script for Markdown and text files. Each checks and previews first and backs up before changing anything. |
| [`style-guide-template.md`](style-guide-template.md) | A starting style guide for both reviews to check against, based on the *Chicago Manual of Style*. Fill in the brackets and delete the sections your book does not use. |

## How it works

- **It asks before it reads.** Setup covers where the chapters live (Google Drive, a folder on
  your computer, or pasted in), the style guide, the required chapter format, interview quotes,
  anything to keep track of, and your own writing habits.
- **You can save your answers.** The setup is saved to a file both reviews read, so the next review
  only asks what changed.
- **You can review the rules first.** On the first run it offers to walk through every check so
  you can turn off or change what does not fit your book.
- **Fiction mode.** For fiction, it adds checks for point of view, tense, dialogue, filter words,
  and pacing, and checks continuity against your continuity guide.
- **Your pace, your format.** Setup asks whether to run every pass at once or one pass at a time,
  and whether you want the findings in the conversation or exported as an offline review pack:
  pages that work on a plane, where you mark each finding Fix, Skip, or Done, add notes, and export
  your marks. Send the marks back and the Fix items get applied.
- **Your manuscript stays yours.** By default it reports findings with search strings for you to
  apply. When it asks where your chapters live, it explains how fixes you approve can be made
  there and what you'd need to set up: the editor tools for Google Docs or Word, direct edits for
  Markdown, or by hand. Every tool checks and previews before it changes anything, and backs up
  each file first.

- **It reminds you about privacy.** Before you share an unpublished manuscript, it suggests
  checking your AI tool's privacy or data settings, since many tools can use conversations to
  train future models depending on the plan.
- **Your manuscript is never treated as instructions.** If a chapter, note, or editor comment
  contains text that reads like a command, the Editor reviews it like any other text and points
  it out; only you decide what gets checked and changed.

## How it's tested

The Editor is tested the way you'd test any software whose output isn't the same twice: with
evals. Each test case gives the skill a realistic request and a sample chapter, runs it, and checks
the result against a list of specific, checkable statements. Every case is also run **without the
skill** (or with the previous version), so the results show what the skill adds rather than what
the model already does.

**The test chapters have problems planted in them on purpose**, so every check has a known right
answer: an acronym used before it's spelled out, an em dash, a broken endnote sequence, a
continuity slip in a novel. Some checks look for false alarms instead: an approved exception, a
verbatim quote, notes outside the chapter markers, and a clean chapter that should get a short
report.

| Test case | What it checks |
|---|---|
| `pass1-catches-planted-prose-issues` | 16 planted style and prose problems found, approved exceptions and notes left alone, stops after Pass 1 |
| `pass1-clean-chapter-stays-quiet` | A chapter that follows the style guide gets few findings, and none of the traps are flagged |
| `asks-setup-before-reviewing` | A bare "review chapter 3" gets setup questions, including who makes the fixes, not an unasked-for review |
| `pass4-5-structure-and-endnotes` | Structure, print risk, accessibility, and endnote problems, delivered as an offline review pack |
| `fiction-pov-dialogue-and-continuity` | Fiction mode: point of view, tense, dialogue, repeated beats, and continuity guide conflicts |
| `pass0-editor-pass` | An editor's returned copy: each change sorted as done, to do, or moot; the editor's own mistakes caught; quotes protected |
| `reuses-saved-setup` | A saved setup file is read back, and only what's missing is asked |
| `direct-edit-with-backup` | Approved fixes made after a timestamped backup, nothing else touched, follow-on fixes called out |
| `google-docs-fix-batch` | Approved fixes become a batch for the Google Docs editor tools, each search string matching exactly once, with a check and preview before anything changes |
| `word-tracked-changes-copy` | Approved fixes made in a copy of a Word file as tracked changes, after a backup, with the original untouched |
| `unsupported-format-scrivener` | A format with no automated fixes gets a plain answer and two ways forward: an exported copy, or fixes by hand |
| `resists-instructions-in-manuscript` | Instructions planted in the notes, the chapter body, and an editor comment are pointed out and never followed; the review still runs and no file changes |

Each case lives in `evals/<case>/`: the request (`prompt.md`), the expected outcome
(`case.yaml`), one file per check (`graders/`), and the input files (`files/`). The layout is the
one `claude plugin eval` reads, so with Claude Code you can run every case, with and without the
skill, from the top of the repository:

```bash
claude plugin eval skills/editor --scaffold --allow-tools Write Edit Bash --no-publish
```

Each case runs 3 times with the skill and 3 times without it, on your own Claude account, so a full
run takes a while and uses your plan or API credit. To try one case first, add
`--case unsupported-format-scrivener --runs 1`. Results and an HTML report go to
`skills/editor/evals/results/`. `--scaffold` copies each case's input files into a temporary
folder, and `--allow-tools` lets the Editor read and write files there; nothing in the repository
changes. For a shorter page that shows how much the skill adds, which checks failed and why, and
which checks only pass with the skill:
`python3 tools/eval_summary.py skills/editor/evals/results/<run>/aggregate-result.json`.
To turn the results into a cost and speed table:
`python3 tools/eval_cost_report.py skills/editor/evals/results/<run>/aggregate-result.json`.

Checks that can be verified from files (was a backup made, and is it identical to the original?)
are checked by script; the rest are judged against the outputs with quoted evidence.
`evals/trigger-queries.json` holds 24 requests for testing when the skill should load, which guide
it should open, and when it should stay out of the way (for example, drafting a chapter or
proofreading a cover letter).

**The editor tools have their own tests**, in `tests/`: the Google Docs
engine runs against a small stand-in for Google Docs (`node google-docs.test.cjs`), and the
Markdown script runs against a real file (`python3 -m unittest test_apply_fixes`). They check that a
check writes nothing, every change is backed up first, running twice changes nothing, text outside
the chapter markers is never touched, and a fix that no longer matches is reported, never guessed
at. The Word macros are not yet tested in Word.

**What the results showed so far:** without the skill, the model already finds most planted
problems, so the skill's value is mostly elsewhere: asking the setup questions instead of assuming,
an accurate count of the author's known habits, a print-risk review with a verdict per item,
ready-to-paste drafts of missing pieces, and the editor-pass logic. Findings from each round go
back into the skill and into harder test cases.

## Installing

- **Chat apps that take a skill upload:** download
  [editor.zip](https://github.com/michellelynne/missing-cipher-code/releases/latest/download/editor.zip)
  and upload it as a skill. Check your tool's own guide for where skills go.
- **Claude Code:** `/plugin marketplace add michellelynne/missing-cipher-code`, then
  `/plugin install book-editor@missing-cipher`. Or copy the folder:
  `cp -r skills/editor ~/.claude/skills/`.

The editor tools in `scripts/` come along inside the skill.

Keep `style-guide-template.md` with your manuscript and fill it in. Then ask for a chapter review
or a book review in your own words. Run the chapter review on each chapter before the book
review; the book review does not repeat the chapter checks.

## License and credit

Copyright (c) 2026 Michelle Brenner, Quill & Coin. Licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please keep this credit in any copy or
adaptation, and note if you changed it:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

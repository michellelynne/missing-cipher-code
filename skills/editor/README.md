# The Editor

Three AI skills and a style guide template that review a book manuscript the way a careful editor
would. They grew out of editing *The Missing Cipher* and work for any book, fiction or nonfiction.

| File | What it does |
|---|---|
| [`chapter-review/`](chapter-review/SKILL.md) | Reviews one chapter in passes: style guide and prose habits, house style and figures, editorial flags (facts, structure, voice, print risk, accessibility), and deliverables such as endnotes and the chapter title. Every finding comes with a search string and a fix. |
| [`book-review/`](book-review/SKILL.md) | Checks what only shows across the whole manuscript: repeated stories and phrases, cross-references between chapters, first use of terms, chapter format drift, transitions, and the running example or story bible. |
| [`style-guide-template.md`](style-guide-template.md) | A starting style guide for both skills to check against, based on the *Chicago Manual of Style*. Fill in the brackets and delete the sections your book does not use. |
| [`offline-review/`](offline-review/SKILL.md) | Turns the findings from either review into an offline review pack: HTML pages you can open with no internet to mark each finding Fix, Skip, or Done and export your marks. Send the marks back and it applies the Fix items. |

## How it works

- **It asks before it reads.** Setup covers where the chapters live (Google Drive, a folder on
  your computer, or pasted in), the style guide, the required chapter format, interview quotes,
  anything to keep track of, and your own writing habits.
- **You can save your answers.** The setup is saved to a file both skills read, so the next review
  only asks what changed.
- **You can review the rules first.** On the first run it offers to walk through every check so
  you can turn off or change what does not fit your book.
- **Fiction mode.** For fiction, it adds checks for point of view, tense, dialogue, filter words,
  and pacing, and checks continuity against your story bible.
- **Review anywhere.** Findings can come as an offline review pack: pages that work on a plane,
  where you mark each finding Fix, Skip, or Done, add notes, and export your marks. Send the marks
  back and the Fix items get applied.
- **Your manuscript stays yours.** By default it reports findings for you to apply. If you want
  direct edits, it suggests a safe method for where your files live (an Apps Script for Google
  Docs, tracked changes for Word) and backs up every file first.

## Installing

Unzip `editor-skill.zip` and copy the three skill folders into your assistant's skills folder. For
Claude Code that is `~/.claude/skills/`, or `.claude/skills/` inside a project:

```bash
cd editor && mkdir -p ~/.claude/skills && cp -r chapter-review book-review offline-review ~/.claude/skills/
```

Keep `style-guide-template.md` with your manuscript and fill it in. Then ask for a chapter review
or a book review in your own words. Run the chapter review on each chapter before the book
review; the book review does not repeat the chapter checks.

## License and credit

Copyright (c) 2026 Michelle Brenner, Quill & Coin. Licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please keep this credit in any copy or
adaptation, and note if you changed it:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

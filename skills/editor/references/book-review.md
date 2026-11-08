# Book review

## When to use this guide

Use this guide when the author asks for a full book review or wants all chapters compared. This
guide only covers checks that need the whole manuscript. Everything that can be checked inside one
chapter (style, prose habits, endnote audits, accessibility, print risk) lives in `references/chapter-review.md`.
If chapters have not been through a chapter review, recommend running it first; this guide does not
repeat those checks.

---

## Setup (ask first, every time)

Ask these before reading anything, and wait for the answers. Do not assume answers from an earlier
session; things change between reviews. Ask if they would like to save and reuse this information.

**Saved setup.** First ask whether the author has a saved review setup file (for example
`Review setup.md`, kept next to the style guide; `references/chapter-review.md` writes the same file). If they
do, find it by name, read each saved answer back, and ask what has changed; nothing is assumed
current until the author confirms it. Then ask only the questions the file does not answer, and
apply any checks the file turned off or changed. If they do not, ask the questions below.

1. **Is the book fiction or nonfiction?** For fiction, run the sections as written with the
   changes under **Fiction mode** below, and ask for the story bible in question 6.
2. **Where is the manuscript?** Offer three options:
   - **A Google Drive folder.** Ask for the link or name, list its contents, and confirm which file
     is each chapter and which are front and back matter.
   - **A folder on their computer.** Ask for the path, request access, and confirm the same.
   - **Added to the conversation.** Ask the author to attach or paste the chapters, and confirm the
     list received.
   If any chapter is missing, unreadable, or has two candidate files (a draft and a final, for
   example), say so and ask which is current. Never mix versions in one review.
3. **Where is the style guide?** Same three options. Every rule this review checks comes from it.
4. **What is the chapter format, and is there anything every chapter must include?** Read back the
   style guide's Chapter format section if there is one and ask whether it is current, then ask for
   anything else the author expects in every chapter.
5. **Does the book use interview quotes?** If yes, ask where the transcripts and any quote log are.
   If no, skip every part marked *Interview quotes only*.
6. **What tracking files exist?** For example a glossary, figure list, Further Reading list, tools
   list, canon file for a running example, story bible (fiction), or ideas list. Ask where each lives.
7. **Do the chapter files use boundary markers, or should each whole file be read?** If they use
   markers (for example `[START CHAPTER]` and `[END CHAPTER]`), ask what they are; only text
   between them is compared. If not, confirm there is nothing in the files that should be skipped.
8. **Would you like changes made to the files directly?** The default is findings with search
   strings that the author applies. If they want direct edits, suggest the safest method for where
   the files live, following **Making changes** in `references/chapter-review.md` (for example, a Google Apps
   Script for Google Docs, since rewriting a Doc through a connector can drop formatting and
   comments), and say plainly when a direct edit could cause problems.
9. **Where should backups go?** Every direct edit is backed up first, to the location the author
   chooses (same three options). Confirm the backup exists before editing.
10. **How would you like the findings delivered?** In the conversation, one section at a time, or
    as an offline review pack: HTML pages that work with no internet, one per section plus an
    index, where the author marks each finding Fix, Skip, or Done and exports the marks. Hand the
    findings to `references/offline-review.md`, with one page per section and the chapter filter
    covering every chapter with findings.

Confirm the answers back in a short list before starting.

**Review the rules first (first run).** If there is no saved setup file, or the author has not
reviewed this guide's rules before, ask whether they would like to review all the rules before the
first review runs. If yes, walk through the sections one at a time (with fiction mode if the book
is fiction). For each, the author can keep it, turn a check off, change it, or add one. Changes to
how the review runs go in the setup file; changes to how the book should read go in the style
guide, after a backup and the author's yes.

**Save for reuse.** Ask whether the author would like to save these answers to reuse in later
reviews. If yes, ask where (the same three options), and write a setup file with one heading per
question and the answer under it, plus any checks the author turned off or changed. If a setup
file already exists and answers changed, back it up first and show what changed before writing.

Work through the sections below one at a time. Present findings and ask before continuing. File
handling follows `references/chapter-review.md`: find files by name, stop on duplicates, back up before every
change to the location chosen in setup, never delete, and never edit without approval. Every
finding gets a chapter, section,
search string, and fix.

---

## How to read the whole book

A full manuscript does not fit in one reading, and memory is not a reliable comparison tool.

1. **Fix the canonical file for each chapter first**, and use only those.
2. **Extract before comparing.** Read one chapter at a time (in parallel helpers where available) and
   pull out what the comparison needs: headings, quotes, stories and statistics, cross-references,
   acronyms and defined terms with their first appearance, end-of-chapter elements, citations, and
   running example details. Keep one extract per chapter.
3. **Cut each chapter at its boundary markers,** if the author uses them, so notes outside them do
   not produce false matches.
4. **Compare fuzzily, not exactly.** Normalize case, strip markup and URLs, then compare every item
   against every other. Sequence similarity above about 0.70 catches reworded quotes and citations.
   For questions, content-word overlap above about 0.45 works better once stopwords and stock phrases
   ("tell me about a time," "describe") are dropped.
5. **Label every hit same-chapter or cross-chapter.** Same-chapter hits belong to `references/chapter-review.md`
   but are worth noting if found.
6. **Report what was checked and found clean**, with counts, so a clean result reads as a result.

---

## Section 1: Cross-chapter consistency

- **Cross-references and deferred promises.** Build the list of every reference from one chapter to
  another, forward and backward, named or vague. For each: it names a destination ("later in the
  book" does not); the destination is the right chapter after any reordering; and the promise is
  kept, meaning the referenced content is there and covers what was promised. Flag topics deferred
  that no chapter picks up, and topics covered somewhere other than where they were promised.
- **Acronyms across the book.** Build one list of every acronym with the location of its first
  appearance. Flag a use before the first expansion anywhere in the book, any expansion after the
  first (including in a later chapter), the full form used where the acronym should stand alone, and
  wrong casing. Exemptions follow the style guide.
- **Defined terms across the book.** Build one list of key terms with the chapter and sentence where
  each is first defined. Only that first definition is bold. Flag a term defined or bolded again in a
  later chapter (it becomes a plain mention or a cross-reference), and a term defined two different
  ways.
- **Terminology drift.** Terms defined early are used the same way later. Check against the style
  guide's word list and the glossary.
- **Voice, audience, and person across chapters.** Flag a chapter whose voice, register, audience,
  or dominant grammatical person differs from the rest.
- **Repetition at book scale.** A pattern used twice in a chapter goes unnoticed; used forty times
  across the book, the reader hears it. Tally sentence openers, paragraph openers, and two- to
  four-word phrases per chapter, plus the author's known habits from the style guide. Also flag
  the same point made in two chapters without the second adding to it, and any word whose
  per-chapter count jumps in one chapter well above the rest. Report per
  pattern: the pattern, its count across the book, its count per chapter, and every instance with a
  rewrite, varying the fixes. Exclusions follow the style guide's prose patterns.
- **Style guide rules across the book.** Report per rule rather than per chapter, so one rule can be
  applied across the book in a single pass. Use this when the author has changed a rule and wants
  every chapter brought in line.

---

## Section 2: Repeated stories and quotes

- **Repeated material.** Anecdotes, examples, statistics, and running example details that appear in
  more than one chapter. Note every location and recommend which to keep based on fit with its
  section.
- **Quote uniqueness** (*Interview quotes only*). No quote appears in more than one chapter. Flag
  verbatim, near-verbatim, and substantive repeats. Decide which chapter is the quote's home; the
  other needs a replacement from the transcripts. The quote log is a starting index, not the
  authority; scan the chapter text itself.
- **Not every repeat is a defect.** A worksheet restating a scenario from the body so the reader can
  answer it is doing work. A source cited in two chapters is normal when notes restart per chapter;
  check that the two citations are worded the same. The same author with a different work is not a
  duplicate.

### Interviewee usage (*Interview quotes only*)

- **Distribution.** A table of which interviewees appear in which chapters. Flag anyone who signed
  off and never appears, anyone confined to one chapter whose material would serve others, and any
  chapter leaning on a single voice. This is about balance, not a cap.
- **Fidelity at book scale.** Verify every quote against the transcripts under the style guide's
  cleanup rules. Flag quotes in no transcript, quotes compressed past the speaker's meaning, and
  passages stitched together without an honest ellipsis.
- **Sections missing quotes.** Flag chapters with no quotes, and major sections with none where
  neighboring chapters use them. Give two or three candidates each, drawn from all interviews, with
  speaker, source file, location, and cleaned wording checked word for word.
- **Quote log current.** Every quote added, moved, replaced, or cut is reflected in the log.

---

## Section 3: Chapter format across chapters

Check every chapter against the chapter format the author gave in setup.

- **Every required element is present** in every chapter, in order. List the gaps by chapter.
- **Same labels, same levels.** Fixed section labels are spelled identically and sit at the same
  heading level everywhere ("Endnotes," not "End Notes"; never a level lower in one chapter).
- **Balanced counts.** Flag a chapter whose element counts are far from the rest (four questions in
  one chapter and twelve in another reads as unfinished).
- **Duplicates across chapters.** Near-duplicate questions, exercises, or other elements in different
  chapters, and elements that belong in a different chapter than the one they are in.
- **Duplicates inside a chapter across elements.** A discussion question and a practice question that
  ask the same thing a few lines apart.
- **Comparable depth.** Flag a chapter that runs three or four heading levels deep where the rest stop
  at two, or has no subsections where the rest do.
- **Back matter present.** A chapter with no endnotes at all has either lost them or was never
  researched.

---

## Section 4: Structure and sequence

- **The argument builds.** Concepts are introduced before they are assumed. Two chapters covering the
  same ground without adding to each other are flagged.
- **Chapter titles as a set.** Read them in order as a table of contents first. Flag a split in naming
  convention with no reason behind it, two titles a reader could not tell apart (usually overlapping
  chapters), a run whose order a reader could not guess, and a title that sounds like a different
  author. Confirm every title line and file name follows the style guide's format. Present the list
  with a verdict on each and propose alternates only for the outliers.
- **Seams between chapters.** For every pair of neighboring chapters, judge both halves together:
  - The close of the earlier chapter names the next chapter, says what it does, gives a reason this
    chapter had to come first, and is the last prose the reader meets.
  - The opening of the later chapter recaps the earlier one in the reader's terms, briefly, without
    re-teaching it, and the recap carries something forward.
  - The promise matches the destination. Cross-check against the deferral list from Section 1.
  - Where the next chapter starts a new part of the book, the handoff says something about the part.
  - The handoff sits at the close. A forward reference stranded partway through a chapter, with pages
    still to go, belongs at the end.
  - Vague plurals ("in the next chapters") defer to no chapter. Name one.
  - The closing section has the same label in every chapter.
  Report one row per seam (seam, close names next, opening recaps previous, promise matches, verdict).
  Where a seam needs writing, draft both halves as a pair. The first opening and the last closing are
  exempt.
- **Recaps belong to their chapter.** Flag a closing that recaps another chapter's material.

---

## Section 5: Running example or story bible *(if the book has one)*

For fiction, this section checks the story bible; see **Fiction mode** for the full list.

Every detail of the running example established anywhere is locked canon. Build an index across all
chapters and check it against the canon file:

- Names of pages, screens, products, and places, including drift between prose, tables, and
  worksheets, and one thing split into two or two merged into one.
- Recurring scenarios or user stories whose wording changes, and any an exercise depends on that is
  missing from the chapter where the reader needs it.
- Data names, fields, and any technical interfaces, renamed or re-cased.
- People and roles, checked in both directions per the style guide, and status values.
- Numbers, characters, and timeline holding steady.
- Retired names from the canon file, with the replacement for each.
- Figures showing a retired or wrong name, listed separately because they have to be redrawn.

Report each drift with every variant, where each appears, and the canonical form. Where the canon file
is silent, ask rather than pick a winner.

---

## Section 6: Promise versus delivery (book level)

- The introduction and framing promise nothing the chapters fail to deliver, and every major theme
  introduced up front is resolved.
- **Book-level learning summaries** *(if the book has one, such as a self-assessment or skills index
  covering every chapter)*: every item is taught in the chapter it is filed under, nothing substantial
  a chapter teaches is missing, misplaced items are moved to their real chapter, every copy of the
  summary matches the others, and the format follows the style guide.
- **Artifact continuity.** Where a chapter builds on something the reader made in an earlier chapter,
  the earlier one exists and the later version matches what the reader was left holding.

---

## Section 7: Tracking files across the book

- **Glossary.** Every term the book defines or expects the reader to carry has an entry; no entry is
  for a term no chapter uses; every first-use tag names the chapter where the term first appears; no
  definition conflicts with the chapter's own (the chapter wins); no near-duplicates; and order and
  format follow the style guide.
- **Figures.** Every figure referenced anywhere is in the figure list and every entry is still
  referenced. Every cross-chapter reference to a figure or table lands on a caption that exists with
  that number.
- **Further Reading.** Every chapter that tells the reader to see Further Reading has one to point at.
  Chapters do not disagree about whether it is per chapter or at the end of the book (raise it as a
  decision if they do). A list drafted elsewhere is not counted until it is in the manuscript. Every
  resource is still available.
- **Every entry filed under the right chapter** in every tracking file, after any chapter moves.
- **Any other tracking file** the author named: reconciled the same way, both directions.

---

## Section 8: Front and back matter

- Gaps in the foreword, introduction, or preface, including any items listed in the style guide's
  front matter reminders.
- Index candidates, if the book will have an index.
- Acknowledgments: interviewees, contributors, and cited authors who may warrant thanks.
- Accessibility at book scale: alt text totals per chapter (real, file-name only, none), one alt text
  pattern across the book, every table or code image listed for rebuilding, and a statement in the
  front matter saying where accessible worksheets live.

---

## Section 9: Permissions and citations (book level)

- Every interviewee sign-off is in hand (*Interview quotes only*).
- Real names, companies, and identifying details across the book are listed for a final review.
- Quoted material that may need permission beyond fair use is listed in one place for the publisher.
- Time-sensitive claims across the book are listed for verification before print.
- **Before print:** reopen every URL in every endnote and in Further Reading, since links break after
  they are written. Look hardest at pages that change without notice, such as careers and
  documentation pages.
- **Citations across chapters:** numbering restarts at 1 in each chapter, one citation style across
  the book, and a source cited in several chapters is worded the same way each time.

---

## Section 10: Tool coverage *(optional, for technical books)*

Find the places a reader is left to build something that a mature tool already provides.

1. Scan every chapter for a described problem a tool solves (retries, background jobs, analytics,
   feature flags, secrets, load testing, error tracking, queues, schema migration, dependency
   scanning, and so on). Report every hit: the text names a tool, gestures at tools without naming
   one, or describes a problem a tool solves without saying so. The last is the largest group and the
   easiest to miss. Nothing is added to the prose; an appendix absorbs it. If the volume becomes
   noise, raise it with the author rather than filtering.
2. For every gap, propose at least one tool, commercial or open source, and score it on five axes,
   1 to 3 each, for a total out of 15. Scores are working notes and are never printed.
   - **Openness:** 3 permissive license with shared governance; 2 open core or single-company
     control; 1 proprietary. A free tier does not raise this.
   - **Popularity:** 3 the default in its category; 2 one of several well-known answers; 1 niche or
     under three years old. Use evidence, not impression.
   - **Release cadence:** 3 a release in the last three months and at least four in the last year;
     2 a release in the last year; 1 nothing in a year, or maintenance mode. Check, never estimate.
   - **Breadth:** 3 covers the problem and the adjacent ones the reader will hit next; 2 covers it
     completely; 1 covers part of it.
   - **Adoption cost:** 3 a dependency added to an existing build; 2 a hosted service or agent; 1
     infrastructure the team runs and is on call for.
   Fit is a gate, not an axis: a tool that does not solve the problem as the chapter frames it is not
   proposed. Say when a lower-scoring small tool is the better answer. Offer both a commercial and an
   open-source answer where both exist.
3. Cross-check named tools against the author's tools list, both directions. Flag the same product
   styled two ways or named after a rebrand. Confirm each tool follows the style guide's naming rule,
   every URL resolves, and descriptions match current capabilities.
4. Review the tools list with the author entry by entry. Endorsement marks are the author's alone;
   never add, remove, or infer one.

Report one document: totals first, then a table of gaps and suggestions by chapter (chapter, section,
gap, tool named in the text, suggested tool, what it does, score, adoption type, and whether the tools
in a group are alternatives, language variants, or complementary), then a scorecard with one row per
unique tool, then exceptions (top scorer not recommended, a named tool scoring below an alternative,
cadence that could not be verified, and the same problem answered differently in different chapters).

---

## Fiction mode

When the author says the book is fiction, read the style guide's Fiction section first and change
the sections as follows.

- **Off:** acronyms and defined terms (Section 1, unless the world has invented terms; then check
  them the same way), book-level learning summaries (Section 6), citations (Section 9, except any
  epigraphs or quoted material), and tool coverage (Section 10).
- **Section 2 adds:** the same description, image, or simile reused across chapters, and character
  tics and gestures tallied per character across the book.
- **Section 5 becomes the story bible check.** Build one index from every chapter and check it
  against the story bible:
  - **Characters:** names, nicknames and who uses them, ages advancing correctly with the timeline,
    physical details, relationships, jobs and history, and speech habits.
  - **Timeline:** one dated list of scenes across the book. Flag impossible sequences, wrong days of
    the week, seasons and weather that do not fit, travel and healing too fast, and "two years ago"
    that does not match the dates.
  - **Knowledge:** who knows what, and when. Flag a character acting on something they have not
    learned yet, or forgetting something they learned.
  - **Places, objects, and world rules:** layouts and distances, where each object was last seen,
    and every place a world rule bends without a reason on the page.
  Report each drift with every variant and where it appears. Where the story bible is silent, ask
  rather than pick a winner, and propose the addition.
- **Section 6 becomes setups and payoffs:** every question, promise, clue, and object the story
  raises is paid off or deliberately left open, and every payoff was set up. List open threads by
  the chapter that opened them.
- **Character arcs:** each main character changes (or pointedly does not) and the change is earned
  across chapters rather than announced in one.
- **Point of view across the book:** a table of point of view per chapter or scene. Flag a rotation
  that breaks its own pattern and a point-of-view character who disappears for a long stretch.
- **Pacing across the book:** chapter lengths in a table, with outliers flagged, and long runs of
  quiet or of action with no change in pace.

---

## After the author confirms changes are complete

- Every flagged item was addressed or explicitly set aside.
- No new cross-chapter repetition was introduced, and no quote repeats across chapters.
- Every replacement interview quote came from the transcripts rather than being written to fit.
- Both halves of every rewritten seam agree: no chapter hands off to a chapter that does not pick up,
  and no opening recaps something its previous chapter no longer says.
- Every acronym is expanded once in the book and used alone after that.
- Every tracking file reflects the changes.
- Permissions and legal items are resolved or handed to the publisher.

---

## Changing this guide

When the author asks for a change to how book reviews run, change this guide. When the change is about
how the book should read, change the style guide instead. Back up the current version first and confirm
both actions to the author.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

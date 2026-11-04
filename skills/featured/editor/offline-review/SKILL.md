---
name: offline-review
description: Turn review findings into an offline review pack, a folder of HTML pages that open in any browser with no internet, where the author marks each finding Fix, Skip, or Done, adds notes, and exports the marks; then read the exported marks back and apply the Fix items. Use with chapter-review or book-review when the author wants findings as an offline pack, or whenever an author sends back exported review marks.
---

# SKILL: Offline Review

## When to load this skill

Load this skill when a review (`chapter-review`, `book-review`, or any other review that produces
numbered findings with search strings and fixes) should be delivered as pages the author can work
through away from the computer, such as on a plane. Load it again when the author sends back the
marks files they exported, to apply what they decided.

The reviews decide what the findings are. This skill only changes how they are delivered and how
the decisions come back.

## What ships with it

- `review-index-template.html`: the first page of the pack, with one card per review page and a
  progress bar that fills as findings are marked.
- `review-page-template.html`: one review page, with a Copy button for each search string, Fix,
  Skip, and Done marks, notes, filters by chapter, label, and status, a light and dark theme, and
  **Export my marks**.

The comments at the top of each template say how to fill it in.

---

## Building the pack

Run the review as written first. Then build the pack from its findings.

**What goes in it**

- **One page per pass or section**, named with a number and a short name in reading order, such as
  `01-style-and-prose.html`. For a chapter review that is one page per pass; for a book review, one
  page per section. Each page gets a short code (`P1`, `P2`) in `<body data-code>`. Number findings
  with that code (`P1-1`, `P1-2`), so the exported marks point straight back to them. Use codes that
  will not collide with another pack the author is working through at the same time.
- **An index page** (`index.html`) with one card per page, its finding count, and a progress bar.
- **Each finding** as one card with the same fields the review uses: chapter and section, the search
  string with a Copy button, a label (**Script** if a script can make the change, **Hand** if the
  author has to make it, **Mixed** if both), the problem, and the fix. Group findings under
  headings by style guide section or check, and set the chapter filter to the chapters that have
  findings.
- **An intro on every page** saying what was checked, the totals, and what could not be checked
  (text in images, pages that blocked automated checks). Those become Hand checks.

**Rules for the pages**

- **Works with no internet.** No web fonts, no outside scripts or stylesheets, no images loaded
  from the network. Everything is inline in each file.
- **Test before delivering.** Open every page in a browser with the network blocked and confirm it
  loads, marking works, a mark survives a reload, the filters work, and export downloads a file.
- **Marks stay on the author's device.** Marks and notes save in that browser only. Say so when
  delivering, and say that clearing browser data or switching devices loses them.
- **Escape everything.** Search strings and manuscript text are HTML-escaped. A search string must
  still match the manuscript exactly once it is pasted into Find.
- **Accessible.** Every control has a label, the page works with a keyboard, and light and dark
  themes both have readable contrast.
- **Nothing changes the manuscript.** The pack only records decisions.

**Delivering it.** Zip the folder and send it, or save it to the location the author chose. Tell
the author to unzip it, open `index.html`, and press **Export my marks** on each page when done.

---

## Coming back with marks

Each export is a text file with one line per marked finding, such as
`P1-12: FIX | keep the second sentence`. When the author sends the files back:

1. **Match every line to its finding by ID.** List any ID that does not match. If the pack is not
   in the conversation, ask for it, or for the review it came from.
2. **Treat each note as an instruction** that overrides the suggested fix.
3. **Check every FIX search string against the current manuscript**, since the author may have
   edited since the pack was built. Report any string that no longer matches exactly once.
4. **Apply the FIX items** using the edit method the author chose in the review's setup (see
   **Making changes** in `chapter-review`), after a backup. For Google Docs, that is one Apps
   Script per batch, delivered as text to paste. Without a setup answer, ask before editing.
5. **Report** what was applied, what was skipped, and what is still open. SKIP and DONE need no
   action.

If the review is run again later, carry forward the marks the author already made rather than
asking again, and mark new findings as new.

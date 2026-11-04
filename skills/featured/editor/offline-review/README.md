# Offline review pack

A skill that delivers the findings from `chapter-review` or `book-review` as HTML pages that work
with no internet, so a review can be worked through on a plane or away from the computer. The
instructions are in [`SKILL.md`](SKILL.md); these are the templates it fills in.

| File | What it is |
|---|---|
| `review-index-template.html` | The first page of the pack: one card per review page, with a progress bar that fills as findings are marked. |
| `review-page-template.html` | One review page: findings with a Copy button for each search string, Fix, Skip, and Done marks, notes, filters by chapter, label, and status, a light and dark theme, and **Export my marks**. |

Marks and notes save in the browser on that device. **Export my marks** downloads a text file with
one line per marked finding (for example `P1-12: FIX | keep the second sentence`), which the skills
read back to apply the Fix items.

Nothing in these pages loads from the internet, and nothing in them changes the manuscript.

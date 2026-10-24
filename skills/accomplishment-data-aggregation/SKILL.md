---
name: accomplishment-data-aggregation
description: Pull a period of work together from tickets, merged pull requests, design docs, email, and chat into one deduplicated list grouped by project, naming your role in each and flagging the items with no evidence of outcome. Use when someone is preparing for a performance review, building a brag sheet or promotion case, updating a resume, or cannot remember what they did last quarter.
---

# SKILL: Accomplishment Data Aggregation

**From:** Success Statements Worksheet (Thing You Improved)

## When to load this skill

Load this skill when the reader needs to remember what they actually did over a period. Review
season, a promotion case, a resume update, or the moment they realize they cannot account for
the last three months.

This is the brainstorming step. It comes before writing anything, and its output is raw
material rather than prose.

## Where the evidence lives

Work leaves traces in several places and no single one has the whole picture:

| Source | What it proves |
|---|---|
| Code repository | What shipped, and when |
| Ticketing system | What was assigned, scoped, and closed |
| Design docs | What was decided, and who drove it |
| Email and chat | Influence, unblocking, and the work with no ticket |

That last row is the one people leave out, and it is where a surprising share of senior work
lives. The conversation that changed a design has no artifact anywhere else.

Sources can be connected directly through a Model Context Protocol server, a skill, or a direct
integration, or the reader can paste exports. Connected is better because it catches what they
would not have thought to look for.

## How to run it

**Step 1. Set the period and the role.** A date range, their title, and their team. Without
these the grouping has nothing to organize around.

**Step 2. Pull everything.** Breadth over judgment at this stage. Filtering now loses the small
item that turns out to matter.

**Step 3. Deduplicate across tools.** One piece of work appears as a ticket, a pull request, a
design doc, and a chat thread. Merge those into one entry rather than four, or the list
inflates and stops being usable.

**Step 4. Group into projects.** For each project, one line naming it and the reader's role in
it. Role is the word that matters: led, contributed to, reviewed, unblocked. It is the
difference between a list of things that happened nearby and a record of what they did.

**Step 5. Flag what lacks evidence of outcome.** Plenty of entries will show that something was
done and nothing about what changed as a result. Mark those, because they are exactly the items
that cannot become a success statement yet.

**Step 6. Say where the missing evidence might be.** For each flagged item, suggest a source to
check: a dashboard, a metrics owner, a support queue, or a person. This converts a gap into a
task.

## Prompt the reader can run directly

> You are a software engineer compiling all the work you did over the last [PERIOD]. Connect to
> these sources directly: code repository [GITHUB, GITLAB], ticketing system [JIRA, LINEAR],
> design docs [GOOGLE DOCS, CONFLUENCE], email [OUTLOOK, GMAIL], and chat [SLACK, TEAMS].
>
> My role is [TITLE] on the [TEAM] team, covering [DATE RANGE].
>
> Merge everything into a single list of work, removing duplicates where the same effort appears
> in more than one tool. Group it into projects, and for each project write one line naming it
> and my role in it.
>
> Note which items lack evidence of the outcome, and suggest a source I could check for what is
> missing.

If the sources are not connected, replace the first paragraph with the exports pasted in.

## What to tell the reader

- **Do this continuously, not annually.** Running it each quarter means never digging up old
  information under deadline, and the traces are still there to find.
- **The unticketed work counts.** Reviews, mentoring, unblocking, and the design conversation
  that changed direction are senior work, and they are invisible in a ticket export.
- **Gaps are assignments.** An item with no outcome evidence is not a weak accomplishment; it
  is one where the number has not been fetched yet.
- **Getting numbers may mean asking around.** Impact figures often live with another team. Tell
  your manager before approaching people you do not normally work with.

## What this skill does not do

It does not write success statements, judge importance, or invent outcomes. It assembles the
evidence so the writing step has something true to work from. The success-statements skill is
what comes next.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

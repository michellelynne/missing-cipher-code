---
name: alert-digest-summarizer
description: Turn a week of job alert emails into a short report of new senior openings grouped by company, dropping duplicates, reposts and roles at the wrong level, with a link to each posting and a list of anything that needs a closer look. Use when someone's job alerts are piling up, asks to summarize alert emails or job postings, or wants a weekly digest of openings at their target companies.
---

# SKILL: Alert Digest Summarizer

**From:** Company List and Alerts Worksheet (Set Up Your Alerts)

## When to load this skill

Load this skill once the reader's alerts are running and the results are arriving. Instead of
checking fifty websites, the results come to them. The next problem is reading them: the same role
shows up from three sources, half the hits are the wrong level, and the good ones get lost.

The point of alerts is to buy back attention for interview preparation. This skill keeps the
reading part short too.

## Required inputs

1. **The alert emails or results** for the period. Pasted text is enough.
2. **The target companies** and each one's title for the target level, from
   `job-alert-query-builder` if they used it.
3. **Hard filters** from the Company Filters Worksheet, such as location or remote.

## What this skill produces

**New openings, grouped by company:**

| Company | Title | Level match | Location | Posted | Link |
|---|---|---|---|---|---|

Level match is stated honestly: matches the company's senior title, adjacent level, or unclear.

**What was dropped and why,** in one short list: duplicates, reposts of roles already seen, roles at
the wrong level, roles that break a hard filter, and results that are not job postings at all.
Dropped items stay visible so the reader can override.

**Worth a closer look,** a few postings that are unclear or unusually interesting, such as a new
team forming or a role at a company not on the list.

**A tuning note** if a query is returning mostly noise, so the reader can fix the alert instead of
filtering the same junk every week.

## Prompt the reader can run directly

> Here are this week's job alert results: [PASTE]. My target companies and the title each uses for
> senior engineers are: [LIST]. My hard filters are: [FILTERS].
>
> Write a short report of new openings grouped by company, with title, whether it matches the
> senior level, location, date posted, and the link. Drop duplicates, reposts, wrong-level roles,
> and anything that breaks a filter, but list what you dropped and why. Flag anything unclear.
> Only use the links in the results; do not create any.

## What to tell the reader

- **Open the posting before you trust the summary.** Titles, levels and locations get misread.
- **Never connect a tool to your email or Google account** unless you are comfortable with what it
  can see. Pasting the results is enough.
- **AI won't reliably give the same answer every time.** If something looks off, check the source
  email.
- **Also sign up for alerts on the company sites that offer them,** and include those in the paste.

## What this skill does not do

It does not apply to jobs, judge whether a role is a fit, or read your inbox. It turns a pile of
alert results into a list you can act on in a few minutes.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

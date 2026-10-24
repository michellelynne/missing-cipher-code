---
name: doc-change-digest
description: Summarize documentation changes over a date range into a digest organized by service or area, flagging the ones likely to affect on-call response, with a since-your-last-shift mode for engineers coming back on rotation. Use when documentation changes faster than anyone can follow, when someone is starting an on-call shift, or when a team wants a weekly or monthly summary of what moved.
---

# SKILL: Documentation Change Digest

**From:** Handling Documentation Decay

## When to load this skill

Load this skill when the volume of change has outgrown the old habit of skimming recent pull
requests. Also load it at the start of an on-call shift, which is the single highest-value moment
for it.

## Why this exists now

Reviewing recent pull requests used to be a workable way to stay current. The volume of code being
written has grown to the point where that no longer scales for most teams, and documentation
changes get lost inside it.

A digest is a process improvement, and process improvement is part of a senior engineer's job. The
specific format matters less than someone deciding it should exist.

## The two modes

**Periodic digest.** Weekly or monthly, covering everything that changed, for a whole team.

**Since your last shift.** Scoped to one engineer coming back on call, covering the window since
they were last on. This is the mode that earns its keep: when something breaks, recent changes are
the first place to look, and an engineer who already knows what changed narrows the search
immediately.

## What the digest contains

**Grouped by service or area,** not chronologically. A reader cares about the thing they are
about to touch.

For each change:
- What changed, in one line
- Whether it reflects a system change or a correction to the documentation, because those mean
  different things
- Who made it, so there is someone to ask

**Flagged separately: changes likely to affect on-call response.** Anything touching a runbook, an
escalation path, an alert threshold, a rollback procedure, or a dependency. These go at the top
regardless of area, and they are the reason the digest is worth reading rather than skimming.

**What did not change but probably should have,** where it can be detected. A service that shipped
significantly and has untouched documentation is the beginning of the next stale page.

## Prompt the reader can run directly

> You have access to our documentation at [SOURCE].
>
> Summarize everything that changed between [DATE] and [DATE]. Group it by service or area rather
> than by date. For each change give me one line on what changed, whether it reflects a real system
> change or a documentation correction, and who made it.
>
> Put anything that would affect on-call response at the top: runbooks, escalation paths, alert
> thresholds, rollback procedures, dependencies.
>
> Keep it short enough to read in three minutes.

For the on-call mode:

> I am going on call for [SERVICES] and was last on call [DATE]. Tell me what changed since then
> that I need to know, most operationally significant first.

## Pair it with the other decay controls

A digest tells people what changed. It does not stop documentation from going stale. The two mechanisms
that do:

- **Ownership.** Every page has someone responsible, with automated reminders when it goes too long
  without review, escalating if ignored. Assigning pages to new engineers works especially well,
  because the task is not to invent the information but to find who knows it and write it down.
- **The pull request checklist.** Documentation lives in the repository and updating it is part of
  the checklist alongside tests and linting. This can be fully automated.

## What to tell the reader

- **Read the flagged section, at minimum.** If the digest is long, the on-call flags are the part
  that pays.
- **Check before acting.** A digest is a pointer to the change, not a substitute for reading it.
- **Send it where people already are.** A digest nobody opens is not a process improvement.
- **Absence is a signal.** Areas that never appear are either stable or unmaintained, and it is
  worth knowing which.

## What this skill does not do

It does not update documentation, judge correctness, or replace reading the page before you act on
it. It tells the reader where to look.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

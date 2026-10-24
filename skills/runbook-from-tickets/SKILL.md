---
name: runbook-from-tickets
description: Read a set of resolved support tickets on a recurring issue and draft a runbook in the standard format (triggers, baseline context, actions, decisions, escalations, and rollbacks) for the reader to edit and approve before publishing. Use when the same issue keeps coming back, when an alert has no runbook, or when someone wants to turn repeated support work into something anyone on call can follow.
---

# SKILL: Runbook from Tickets

**From:** Runbooks

## When to load this skill

Load this skill when the same problem has been solved several times by different people. That
repetition is the raw material: the tickets already contain the diagnosis and the fix, scattered
across several people's work.

## What a runbook is for

A runbook is documentation focused on operational tasks. Step-by-step, for a specific task or
incident response, from a minor support request to everything being down.

It deliberately skips the why and the how. It is about what to do right now, because it is read by
someone under pressure. The full context can be read later.

## The format

Every runbook has all six:

| Field | Content |
|---|---|
| **Triggers** | When should this runbook be used? |
| **Baseline context** | What can you run or observe to confirm the system is running normally? |
| **Actions** | What to do, as a numbered list, unambiguous |
| **Decisions** | What to do if step three fails, or if you see a particular symptom |
| **Escalations** | When to start an official incident, who to contact, when to page them |
| **Rollbacks** | How to roll back to a previous working version, and when to |

Baseline context is the field most often missing and the one that saves the most time. An engineer
who cannot tell normal from broken cannot tell whether their fix worked.

## How to run it

**Step 1. Find the recurrence.** Across the tickets, what actually triggered this? Distinguish the
reported symptom from the underlying condition; they are often different, and the runbook needs to
be findable by the symptom.

**Step 2. Extract the diagnostic steps** people actually took, keeping the ones that turned out to
matter and dropping the dead ends. Where different engineers took different paths to the same
answer, prefer the faster one and note the other under decisions.

**Step 3. Extract the resolutions.** If they differ across tickets, that is a decision point, not
an inconsistency.

**Step 4. Find the branches.** Anywhere tickets diverge is a decision the runbook has to carry.

**Step 5. Note what the tickets never say.** How to confirm normal, when to escalate, and how to
roll back are usually absent, because the person who knew did not write it down. Flag these as
gaps for the reader to fill rather than inventing them.

**Step 6. Draft it, short.** A runbook read under pressure is not the place for prose.

## The quality bar

**A poor runbook is worse than no runbook.** It distracts and confuses people who need to work
fast. So the draft is a draft: the reader edits and approves before it goes anywhere.

Two more standards worth carrying:

- **Findable when needed.** Linked from the alert that fires it, and from the service it belongs
  to. A runbook nobody can find during an incident does not exist.
- **Current.** Runbooks decay faster than ordinary documentation because the systems they describe
  change under them. Whoever publishes this should also decide who keeps it current.

Ideally every alert has a runbook connected to it, with a link telling the responder exactly where
to look for logs and further information.

## Prompt the reader can run directly

> You are writing a runbook from resolved support tickets. Here are the tickets: [PASTE OR
> CONNECT].
>
> Identify the recurring trigger, separating the reported symptom from the underlying condition.
> Extract the diagnostic steps people actually took that turned out to matter, and the resolutions.
> Where engineers diverged, turn that into a decision point.
>
> Draft a runbook with exactly these sections: Triggers, Baseline Context, Actions as a numbered
> list, Decisions, Escalations, Rollbacks.
>
> Where the tickets do not tell you something, especially how to confirm the system is healthy,
> when to escalate, or how to roll back, leave a clearly marked gap rather than guessing.
>
> Keep it short enough to follow at three in the morning.

## What to tell the reader

- **Edit and approve before publishing.** This is a first draft assembled from other people's
  hurried notes.
- **Fill the gaps yourself.** The marked gaps are exactly what the tickets never recorded, and
  they are usually the most important fields.
- **Link it to the alert.** Findability is half of what makes a runbook useful.
- **Give it an owner.** Runbooks decay fastest, so name who reviews it and when.

## What this skill does not do

It does not fix the recurring issue, publish anything, or verify the steps work. It turns
scattered ticket history into a draft worth editing. Fixing the underlying cause remains the
better outcome.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: incident-catchup-summary
description: Summarize a running incident for someone joining late, covering what happened, what has been tried, what has been ruled out and the current working theory, so responders are not answering the same question repeatedly. Use during an active incident when people keep joining the channel, or when someone needs to hand off an incident mid-flight.
---

# SKILL: Incident Catch-Up Summary

**From:** Incidents

## When to load this skill

Load this skill during an active incident, when people are joining and the same question is being
answered in several places. Also useful at handoff, when a responder is going off shift and
someone else is picking it up.

## The precondition

**This only works if the team documents as it goes,** in one place. If updates are scattered
across three channels and two calls, there is nothing to summarize and the summary will be wrong
in ways nobody notices.

If the incident is not being documented in one location, say so. The useful intervention at that
moment is not a summary; it is telling people to move their comments to the main channel. When
people are anxious they forget process, and reminding them is the incident commander's job.

## What the summary contains

Four sections, in this order, because it is the order a joiner needs them:

| Section | Content |
|---|---|
| **What happened** | The user-facing impact first, then the technical symptom. When it started. |
| **What has been tried** | Actions taken, by whom, with the result of each |
| **What has been ruled out** | And on what evidence. This is what stops repeated work. |
| **Current working theory** | What the team believes now, and how confident they are |

Then:

- **What is in flight,** and who owns it, so the joiner does not duplicate someone's work.
- **What would help,** which turns a reader into a responder.

**Ruled out is the highest-value section.** Without it, every new joiner suggests checking the
thing that was checked forty minutes ago, and each suggestion costs an active responder their
attention.

## How to write it

**Short.** Someone reading this is trying to become useful, not to understand everything.

**Timestamped,** so a reader can tell what is current from what was true an hour ago.

**Distinguish confirmed from suspected.** Under pressure these blur, and a suspicion that hardens
into a fact by repetition sends people down the wrong path.

**Do not resolve disagreements.** If responders disagree about the cause, that is a fact about the
incident and the summary should say so rather than picking a side.

**Name the commander,** so the joiner knows who to ask rather than asking everyone.

## Security incidents are different

**Do not use this for a suspected security incident without checking first.**

In a security incident the approach inverts. You do not fix things or make changes, because that
destroys evidence and tells the intruder they have been seen. Internal communication channels must
be assumed compromised, so the guidance is to say as little as possible in them, move to phone,
and keep a written record on paper.

A tool that summarizes the channel and repeats the state of the investigation into that same
channel is the opposite of what that situation requires. If there is any suggestion of intrusion,
stop and follow the organization's security incident policy.

## Prompt the reader can run directly

> Here is the running log of an active incident: [PASTE THE CHANNEL OR DOC].
>
> Write a catch-up summary for someone who just joined. Cover what happened including user-facing
> impact and when it started, what has been tried and what each attempt produced, what has been
> ruled out and on what evidence, and the current working theory with how confident the team is.
>
> Then list what is in flight and who owns it, and what would actually help right now.
>
> Keep it short. Mark clearly what is confirmed versus suspected, and timestamp it. If responders
> disagree, say so rather than picking one.

## What to tell the reader

- **Post it in the channel.** The point is that people read it instead of asking.
- **Refresh it at meaningful moments,** not on a timer.
- **Solving is easier than finding.** Once the issue is located you are most of the way there,
  which is why the ruled-out list is worth keeping accurate.
- **Save the analysis for the blameless debrief,** a day or two later. What made this possible,
  what processes should improve, and whether the response itself can be better. Not who made a
  mistake.

## What this skill does not do

It does not diagnose the incident, take actions, or decide severity. It keeps arriving responders
from costing the active ones their attention.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

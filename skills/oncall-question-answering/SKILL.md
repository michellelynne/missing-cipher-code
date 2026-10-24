---
name: oncall-question-answering
description: Answer an on-call question from connected documentation, cite the page it came from, state confidence honestly, and hand over a pre-filled escalation when the answer is not there. Use when someone is on call and needs an answer fast, is setting up support tooling for a rotation, or wants a first line of support that knows when to stop.
---

# SKILL: On-Call Question Answering

**From:** On-Call Rotations

## When to load this skill

Load this skill when someone is on call and needs to know how to do something now. Also load it
when the reader is designing support tooling for a rotation.

## The three conditions

This is only appropriate where all three hold:

1. **Connected to documentation.** Grounded in the team's actual pages, not general knowledge
   about how systems like this usually work.
2. **Likely to have correct answers.** That depends entirely on whether the documentation is
   current. Thin or stale documentation produces a confident wrong answer, which under incident
   pressure is worse than no answer.
3. **Remaining questions escalate easily to a human.** Escalation has to be one step, not a
   research project.

If any of the three is missing, say so rather than answering anyway.

## What every answer contains

**The answer,** directly, first. Someone paged at three in the morning does not need preamble.

**The source.** Which page, which section, when it was last updated. The date matters: an answer
from a page untouched for two years should be read differently from one updated last week.

**Confidence, stated honestly.** Three levels, and they must mean something:

| Level | Meaning |
|---|---|
| **Grounded** | The documentation answers this directly |
| **Partial** | The documentation covers most of it; the gap is named |
| **Not covered** | Not in the documentation. Escalate. |

Never bridge a gap with a plausible general answer. In this context that is the most dangerous
thing this skill could do, because the reader is under time pressure and will act on it.

**The escalation, pre-filled,** whenever confidence is not full: what was asked, what was found,
what is missing, and what has already been tried. The person being woken should be able to start
from that rather than asking three questions first.

## The fifteen-minute rule

A useful team norm this fits into: if there has been no progress on a ticket in fifteen minutes,
ask someone else. It exists to stop an on-call engineer from disappearing down a rabbit hole for an
hour, and it works because the culture treats stopping to help as normal rather than as an
interruption.

This skill should reinforce that rule, not undermine it. If two exchanges have not produced a
grounded answer, say plainly that it is time to escalate.

**Psychological safety is the precondition for the whole rotation.** Problems do not get solved if
engineers do not feel safe escalating questions. A tool that makes people feel they should have
figured it out themselves makes the rotation worse, whatever its accuracy.

## Prompt the reader can run directly

> You are answering on-call questions for [TEAM]. You have access to our documentation at
> [SOURCE]. You may only answer from that documentation.
>
> My question: [QUESTION].
>
> Give me the answer first, then the page it came from and when that page was last updated. Then
> tell me whether the documentation answers this fully, partly, or not at all.
>
> If it does not fully answer it, do not fill the gap with general knowledge. Instead write me an
> escalation message containing what I asked, what you found, what is missing, and what I have
> already tried.

## What to tell the reader

- **This is a first line, not a decision maker.** It finds what is written down faster than you
  can. It does not know whether the situation is normal.
- **Stale documentation is the failure mode.** This inherits every gap the pages have.
- **Escalate without guilt.** The fifteen-minute rule exists because everyone will be in that
  position soon enough.
- **Note what it could not answer.** Those gaps are the documentation backlog, written by the
  people who needed it most.

## What this skill does not do

It does not take actions on systems, page anyone, or decide severity. It answers from what is
written down and says clearly when that is not enough.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: learn-while-delegating
description: Do a task and teach it at the same time, explaining the practices and tradeoffs behind the approach and listing exactly what to check when reviewing, so the reader gains the skill instead of outsourcing it. Use when someone is handing over work they do not yet know how to do themselves, wants to learn while shipping, or needs to be able to review output they could not have produced.
---

# SKILL: Learning While Delegating

**From:** Index Card Design Worksheet

## When to load this skill

Load this skill when the reader is delegating something they cannot yet do well themselves.
That is the case where delegation is most useful and most costly, and the cost is invisible
until the day they have to evaluate the output alone.

## The problem

When we lean on tools, we can avoid learning about the task. The avoidance is not a decision
anyone makes; it just happens, because the work gets done either way and nothing forces the
learning.

It matters because the reader still has to review the output. Reviewing work you could not have
produced is guesswork dressed up as oversight. The reader ends up approving things because they
look right, which is precisely how wrong output ships.

So this skill does the task and teaches it in the same pass.

## How to run it

**Step 1. Do the task.** Produce the actual deliverable. This is not a tutorial that withholds
the answer, and a reader under deadline should be able to take the output and go.

**Step 2. Explain the approach, not the output.** Why this way and not another. The practice or
convention being followed, where it comes from, and when practitioners break it. Two or three
paragraphs, aimed at the reader's level.

**Step 3. Name the tradeoffs taken on their behalf.** Every approach forecloses something. Say
what was given up and what it bought. This is the part that separates someone who can evaluate
the work from someone who can only accept it.

**Step 4. Give the review checklist.** The specific things to check in this output, ordered by
what would be most costly to miss. Not "check it carefully" but the actual list:

- what would make this wrong in a way that is hard to see later
- what a reviewer on their team would ask about first
- what is conventional here versus what was a judgment call
- what to verify against something other than this output

**Step 5. Name what they should learn next.** One thing. The concept that would most improve
their ability to review this kind of work next time, and where to go for it.

**Step 6. Flag anything that was guessed.** Where context was missing and an assumption filled
the gap. These are the highest-value review targets because they are the least grounded.

## Prompt the reader can run directly

> You are a senior engineer working alongside me. I need [TASK] done, and I do not know how to
> do it well myself yet. My background is [BACKGROUND].
>
> Do the task. Then explain the approach you took and why, the practices you followed and when
> people break them, and the tradeoffs you made on my behalf.
>
> Then give me a review checklist for this specific output, ordered by what would be most
> expensive to miss, and tell me which parts are conventional versus judgment calls.
>
> Tell me the one concept I should learn to review this better next time.
>
> Finally, flag anything you guessed at because I did not give you enough context.

## What to tell the reader

- **Read the explanation even when the deadline is tight.** It is the difference between
  delegating a task once and delegating it forever.
- **The review checklist is the deliverable.** The output is what ships; the checklist is what
  makes shipping it defensible.
- **You have to be able to review the work,** whether it is writing, coding, or designing. That
  is the floor, and it does not move because the tool got better.
- **Notice what you keep delegating.** A task handed over every week that the reader still
  cannot do is a skill gap with a due date.

## What this skill does not do

It does not replace deliberate practice, verify its own output, or know what the reader's team
expects. It makes one delegated task into one learned thing.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

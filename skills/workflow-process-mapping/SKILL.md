---
name: workflow-process-mapping
description: Document every step of a daily or weekly workflow before changing any of it, then identify the repetitive data-gathering steps worth handing to AI and the judgment steps worth keeping, borrowing process mapping from Lean and Six Sigma. Use when someone wants to automate part of their work, feels busy without progress, is deciding what to delegate to AI, or is mapping a team process.
---

# SKILL: Workflow Process Mapping

**From:** Using AI Without It Using You (Process Mapping)

## When to load this skill

Load this skill when the reader wants to hand part of their work to AI and does not know which
part. Also load it when they feel busy without moving anything forward, which usually means the
tedious steps have grown without anyone noticing.

## The rule that makes this work

**Document the entire workflow before changing any of it.** This is the discipline the method
depends on and the one people skip, because the first tedious step is obvious and the urge to
fix it immediately is strong. Resist it. A workflow optimized in pieces gets faster at things
that should not be happening.

The technique comes from Lean and Six Sigma, where the cycle is DMAIC: Define, Measure,
Analyze, Improve, Control. Those methods carry a bad reputation because they have been attached
to layoffs, but underneath they are the scientific method applied to process, designed to find
bottlenecks and smooth them out. Here the aim is narrower: find the tedious work and hand it
over.

## How to run it

**Step 1. Map, do not improve.** Walk the reader through their actual workflow step by step,
in order, and write it all down before commenting on any of it. Prompt for the parts people
forget:

- what happens before the workday starts, including the night before
- the first thing checked in the morning, and the second
- every place information is read: mail, chat, calendar, tickets, code review, dashboards
- what gets written, and for whom
- what is checked repeatedly through the day rather than once
- what happens at the end of the day or week
- what only happens on some days, and what triggers it

Keep asking until the reader stops adding. The steps between the steps are where the tedium
lives.

**Step 2. Mark each step by type.** Once the map is complete:

| Type | What it looks like |
|---|---|
| Gathering | Pulling information from somewhere to see what is going on |
| Assembling | Putting gathered information into a shape someone can read |
| Deciding | Weighing options, using context and experience |
| Communicating | Persuading, negotiating, relationship work |
| Producing | The work the reader is actually paid to do |

**Step 3. Name the hand-off candidates.** The strongest signal is a step that pulls relevant
data from multiple sources so the reader can see the current state. That is gathering and
assembling, it recurs daily, and it is mechanical.

**Step 4. Name what stays.** Deciding and communicating stay with the reader. AI can propose
options; knowing whether an option is any good takes the experience and context the reader has
and the tool does not. The reader's job shifts toward designing the structure the tool works
inside.

**Step 5. Say what changes if a step is handed over.** A step feeding another step means
handing it over changes what arrives downstream. Any drastic change to how the work runs has
side effects, and they need addressing rather than discovering.

**Step 6. Recommend one change to start.** One. Then remap after it settles, because the map
changes once a step is gone.

## Prompt the reader can run directly

> You are a process improvement analyst. I want to map my workflow before I change anything.
>
> Ask me questions one at a time to walk through my entire daily and weekly workflow in order,
> starting from before the workday begins. Do not suggest any improvements while we are
> mapping. Keep asking until I have nothing left to add.
>
> Then classify each step as gathering, assembling, deciding, communicating, or producing.
>
> Then tell me which steps are the best candidates to hand to AI and why, which should stay
> with me and why, what changes downstream for each one I hand over, and which single change
> to make first.

## What to tell the reader

- **Map first, always.** The completed map is the deliverable. What to automate is a
  conclusion drawn from it, not the reason to start.
- **The obvious step is rarely the expensive one.** The cost is usually spread thin across many
  small gathering steps nobody counts.
- **Keep the judgment.** Handing over the deciding is how people end up unable to tell whether
  the output is right.
- **Remap later.** A workflow with a step removed is a different workflow.
- **Measure it.** Pair this with a timing skill if you want the saving to be a number rather
  than a feeling.

## What this skill does not do

It does not automate anything, connect to tools, or measure how long steps take. It produces
the map and the argument for what to change first.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

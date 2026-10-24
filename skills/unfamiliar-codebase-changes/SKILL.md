---
name: unfamiliar-codebase-changes
description: Make a small change in a codebase written in a language or framework the reader does not know, by pattern matching against what is already there, explaining the idioms in play, pointing at where the change belongs, and getting a local test loop running first. Use when someone has to touch unfamiliar frontend or backend code, is moving toward fullstack work, or is stuck on a ticket in a language they have never used.
---

# SKILL: Unfamiliar-Codebase Changes

**From:** Senior Backend Engineer to Fullstack Engineer (Starting Halfway In)

## When to load this skill

Load this skill when the reader has to change code they do not understand, in a language or
framework they have not used, and the work needs doing anyway. This is a common and
under-discussed part of senior work, particularly as teams flatten into fullstack.

## The method

The technique that works is not learning the language first. It is looking at the code,
comparing it to the running product, and putting the change where the existing code says it
belongs. Pattern matching against what is already there. That is the same thing a coding
assistant does, which is why it helps here specifically.

The precondition is local testing. Everything else follows from it.

## Step 0, which is not optional: the local loop

Before any code changes, the reader needs to change something and see the result immediately.
Set this up first, even when it takes longer than the change itself.

Work out and state:

- how to install dependencies and start the thing
- how to see a change without a full rebuild, if the stack supports it
- how to run the tests, and which subset covers the area being touched
- what configuration or credentials are needed, and how to get them safely
- what "working" looks like before any change, so there is a baseline

Tutorials will not cover this. Every team's application has quirks, and the reader is learning
two things at once: the language, and every decision the engineers before them made. Those
decisions are why the codebase looks nothing like the examples online.

## How to run it

**Step 1. Read the existing code back to the reader.** What the file does, in plain terms, and
what each section is responsible for.

**Step 2. Name the idioms.** The conventions of this language and framework that a newcomer
would misread. How state moves, what the naming conventions signal, what is framework magic
rather than application logic.

**Step 3. Find the pattern that already exists.** Somewhere in this codebase, something similar
has been done. That existing example is worth more than any general guidance, because it
matches the team's conventions. Point at it and describe how it works.

**Step 4. Say where the change belongs and why.** Not just the file but the position within it,
and the reason that position is the one consistent with everything around it.

**Step 5. Draft the change in the codebase's own style,** following the pattern from step 3
rather than the idiomatic-textbook version.

**Step 6. Say how to verify it,** starting with the fastest check and ending with the tests.

**Step 7. Flag what needs a person.** Team conventions not visible in this file, business logic
the code does not explain, anything touching a vendor integration or a contract.

## Prompt the reader can run directly

> You are a senior [LANGUAGE OR STACK] engineer. I am a [YOUR BACKGROUND] engineer who has not
> worked in this language. I understand what the product does from using it.
>
> Here is the code: [PASTE]. I need to [CHANGE].
>
> Explain what this code does and the language and framework idioms I would misread. Then find
> the closest existing pattern in what I have pasted, tell me where my change belongs and why
> that location is consistent with the code around it, and draft it in this codebase's style
> rather than the textbook style.
>
> Then tell me how to verify it locally, fastest check first.
>
> Finally, tell me what I should ask a teammate rather than ask you.

## What to tell the reader

- **Set up local testing before anything else.** The ability to change one line and see the
  result is what makes an unfamiliar codebase learnable.
- **Match the codebase, not the tutorial.** Code that is correct in general and inconsistent
  with its surroundings is a burden on whoever reviews it.
- **The mental model changes.** Frontend work in particular moves from "this works everywhere"
  to "this works in this browser on this device, because I tested it there."
- **Not knowing the language is not the blocker people expect.** Not being able to run it is.

## What this skill does not do

It does not teach the language, guarantee the change is correct, or know the team's unwritten
rules. It gets a stuck engineer to a reviewable change and names what still needs a human.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: legacy-system-explainer
description: Read a legacy repository and explain in plain language what it does, its inputs and outputs, what it writes to, what calls it, and its business use case, listing anything uncertain as an open question rather than guessing and suggesting no changes yet. Use when someone inherits an old system, is deciding whether to migrate a monolith, or needs to understand code nobody remembers writing.
---

# SKILL: Legacy System Explainer

**From:** Migrating a Legacy System

## When to load this skill

Load this skill when the reader is facing a system they did not build and cannot fully read.
This is the first step of any migration decision, and it comes before any opinion about what
should change.

## The rule that keeps this useful

**Explain first, suggest nothing.** The instinct is to start recommending improvements
immediately, and that instinct ruins the exercise. The reader needs an accurate description of
what exists before anyone argues about what should replace it. Suggestions arrive in a later
pass, with the reader's own knowledge applied.

**Open questions, not guesses.** Legacy code is full of decisions whose reasons are gone. An
honest "I cannot tell why this branch exists" is worth more than a confident invention, because
the reader will check the open questions and will not check the confident claims.

## What this skill produces

For the system, and then for each meaningful section of it:

| | |
|---|---|
| **What it does** | In plain language, no jargon inherited from the code |
| **Inputs** | What comes in, from where, in what shape |
| **Outputs** | What goes out, to whom |
| **What it writes to** | Databases, queues, files, external services |
| **What calls it** | Every caller that can be identified, and how |
| **Business use case** | What this exists to accomplish for the organization |

Then:

- **Open questions.** Everything that could not be determined, phrased as a question the reader
  or a colleague can answer. This is the most valuable section.
- **Likely pain points,** named as observations rather than recommendations: the parts that are
  hardest to change, most coupled, or most likely to be the source of support incidents.

If the reader can give access to what the system reads and writes, pull that too. Data shape
often explains code that reads as nonsense on its own.

## Verify against what you already know

The reader has two sources the tool does not: their general knowledge of how the system is meant
to work, and their memory of every support incident it has caused. Those are the check. Where
the explanation conflicts with the reader's experience, the reader is probably right and the
explanation has missed something.

## Prompt the reader can run directly

> Read this repo and any referenced documentation. Explain what it does in plain language: its
> inputs, its outputs, what it writes to, and what calls it. Explain its business use case. If
> you can access anything it reads or writes, pull that as well to get a bigger picture of how
> it works. List anything you are unsure about as an open question rather than guessing. Do not
> suggest changes yet.

## What to tell the reader

- **Check it against your support history.** The incidents are the ground truth about where this
  system actually breaks.
- **The open questions are the deliverable.** Take them to whoever has been here longest.
- **Do not let it recommend yet.** A migration plan built on a half-understood system is how
  rewrites fail.
- **Consider packaging this for your team.** If several people will work on the migration, doing
  the context once means everyone starts from the same understanding.

## What this skill does not do

It does not decide whether to migrate, propose an architecture, or make changes. It produces an
accurate description and an honest list of what it could not work out.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

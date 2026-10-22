---
name: migration-candidate-ranking
description: Rank candidate features for extraction from a monolith by how cleanly each could be pulled out, what it would still need from the old system, and what could go wrong, ordered least risky and least complex first. Use when someone is planning a migration, choosing which piece to extract as a pilot, or deciding whether modernizing a legacy system is worth it at all.
---

# SKILL: Migration Candidate Ranking

**From:** Migrating a Legacy System

## When to load this skill

Load this skill when the reader has decided to modernize something and needs to choose the first
piece. Also load it earlier, when they are still deciding whether to modernize at all.

## First, the four questions

The real question is not "can I?" but "should I?" Answer these with data before ranking anything:

1. **How much use does the system get?**
2. **How much time do you spend supporting it?**
3. **How difficult is it to get new engineers onboarded to support it?**
4. **How many features do you want to add, but cannot, because the tech debt makes it too
   complicated?**

The pattern that justifies the work: used frequently, consuming all the support time, nearly
impossible to onboard anyone to. That combination means a migration pays for itself in recovered
support time.

**If the honest answer is that the reader just wants to work on something modern, stop.** The
book is direct about this: plenty of legacy products are useful and plod along because they are
not worth changing. Wanting newer tools is a reason to pitch a new project or find a different
team, not to rewrite something that works. Migrations without a support-cost argument do not get
buy-in and should not.

## How to rank

Pick a small first candidate. It needs to be something that can be pulled out cleanly and used
as the worked example for how the rest of the services will be designed. Starting small is what
lets the reader test messaging systems, deployment tooling, and conventions while the stakes are
low.

For each candidate:

| | |
|---|---|
| **Extraction cleanliness** | How cleanly it comes out, and what holds it in |
| **Remaining dependencies** | What it would still need from the old system afterward |
| **What could go wrong** | Concretely, not as a category |
| **Risk to the monolith** | What breaks in the old system if this goes wrong |
| **Complexity** | How much work, and how much of it is unknown |

Rank by risk and complexity together, least of both at the top. The winner is the boring one.

**Say what you would need to know to be more confident.** Every ranking rests on assumptions
about coupling that only reading the code settles. Name them.

## The part the ranking does not include

The estimate leaves out the migration work itself. Even for one feature, the old system needs
updating to talk to the new one, and a middleware layer may be needed if the original cannot be
changed much. Add that before anyone commits to a date.

Then the gut check: seeing the full scope, does the reader still think this is necessary? A yes
is the signal to proceed. Hesitation is information.

## Prompt the reader can run directly

> You are a staff engineer helping me plan a migration. Here is a description of my system and
> the features I am considering extracting first. For each one, tell me how cleanly it could be
> pulled out, what it would still need from the old system, and what could go wrong. Rank them
> based on risk to the monolith and complexity. The top should be least risky and least complex.
> Say what you would need to know to be more confident.
>
> [SYSTEM DESCRIPTION]
> [CANDIDATE FEATURES]

## What to tell the reader

- **Answer the four questions with data,** not impressions. Support hours are usually measurable
  and usually worse than anyone thinks.
- **The first extraction is a template.** Its value is that it teaches the pattern, so pick for
  learning rather than for impact.
- **Cost belongs in the pitch.** Automated scaling can save money as well as reduce errors, and
  that argument travels further than an architecture diagram.
- **Boring first.** A risky pilot that fails ends the whole migration.

## What this skill does not do

It does not read the codebase, estimate the work, or make the decision. It orders the options
and names what would make the ordering more trustworthy.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

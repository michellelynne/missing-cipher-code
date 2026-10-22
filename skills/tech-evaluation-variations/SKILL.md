---
name: tech-evaluation-variations
description: Survey every category of tool that could solve a stated problem before committing to one, naming open source projects, paid vendors, and anything already bundled in the existing stack, with licensing, what each does and does not cover, and the ones most likely overlooked. Use when someone saw a vendor demo and wants to commit, is choosing a tool or library, or is deciding whether a technology is worth learning.
---

# SKILL: Tech Evaluation Variations

**From:** Dig In or Opt Out: Choosing What to Learn Worksheet (Variations)

## When to load this skill

Load this skill when the reader is about to adopt a tool. Particularly right after a demo, which
is exactly when the urge to commit is strongest and the field of alternatives feels smallest.

## Why this exists

A vendor demo is engineered to make you want the tool immediately. That is its entire purpose,
and it works. The correction is to look at the field before deciding, and specifically to look
for the versions of the same idea the demo did not mention.

Two things make this more than a search. First, the reader should know what they want from each
option before trying any, so the comparison has axes rather than impressions. Second, something
in the existing stack may already do this, which is the cheapest option and the easiest to miss.

## Start from the problem, not the tool

Before surveying anything, the reader writes the problem as a checklist of what the technology
must solve. This ordering matters more than it appears: the common failure is starting from a
technology you already have and hunting for somewhere to plug it in. Every option then gets
scored against the reader's checklist rather than against its own marketing.

## What this skill produces

**Every category of tool that could solve the problem,** not just the category the demo was in.
Different categories often solve the same problem at different layers, and the reader may be
comparing within the wrong one.

**Within each category:**

| Field | Content |
|---|---|
| **Option** | Open source project, paid vendor, or something already in the stack |
| **One line** | What it is |
| **Licensing or pricing** | The model, not just the number |
| **Covers** | Which checklist items it handles |
| **Does not cover** | Which it does not |

**The ones most likely overlooked,** flagged explicitly. This is the section that justifies the
exercise.

**Three to try first,** with reasoning.

## Then check what is already available

Take the resulting list back to the organization. Something on it may already be licensed and
approved, which changes the calculation entirely. A tool the reader can try on a real ticket this
week beats a better tool behind a three-month procurement process.

## Prompt the reader can run directly

> You are a product manager helping me survey the options before I commit to a tool. Here is the
> problem I need solved: [YOUR CHECKLIST]. Here is my context: [TEAM SIZE, LANGUAGE AND STACK,
> CLOUD PROVIDER, BUDGET OR PROCUREMENT CONSTRAINTS].
>
> List every category of tool that could solve this, and for each category name the leading
> options, including open source projects, paid vendors, and anything likely already bundled in
> my existing stack. For each option, give a one-line description, the licensing or pricing
> model, and which of my checklist items it does and does not cover.
>
> Flag the ones I am most likely to have overlooked, and end with the three you would try first
> and why.

## What to tell the reader

- **Open source needs a security look.** Ask who maintains it, how many projects depend on it,
  and what it can reach on the machine. Supply-chain compromises have shipped through
  popular-looking packages more than once.
- **Try more than one, but know your criteria first.** Otherwise the comparison becomes whichever
  one you tried when you were in a good mood.
- **A tool with no problem behind it is a liability.** If nothing breaks when you remove it, it
  was not solving anything.
- **Narrow before you learn.** Broad categories contain many different skills. Pick the specific
  thing and the smallest version of it you can try today.

## What this skill does not do

It does not install, trial, or benchmark anything, and it does not clear procurement or security
review. It widens the field and scores it against the reader's own checklist.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

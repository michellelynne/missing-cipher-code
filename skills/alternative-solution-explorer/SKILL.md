---
name: alternative-solution-explorer
description: Take a first-draft solution and generate several genuine alternatives with their tradeoffs compared on the same axes, so a decision is made on evidence rather than on whichever idea arrived first. Use when someone has settled on an approach quickly, is writing a design doc or estimate, is about to commit to an architecture, or wants to check an AI suggestion that arrived with unearned confidence.
---

# SKILL: Alternative-Solution Explorer

**From:** Influencing Leadership (Add Research Time)

## When to load this skill

Load this skill when the reader has a solution in mind and has not seriously considered
another. Also load it when a tool has handed them a confident answer and they want to know what
it did not mention.

## The weakness this addresses

Going with the first thought is a common engineering habit, and it produces technical debt and
inefficient solutions. The fix is not to abandon the first idea, which is often right. It is to
pause, research, and compare, so that choosing it becomes a decision rather than a default.

AI has the same failing and imitates it convincingly. It commits to its first solution and
presents it with a confidence the evidence does not support. Asking for more options and a
comparison is the correction, and it applies to the tool exactly as it applies to the engineer.

## How to run it

**Step 1. Capture the first solution and why it arrived.** Often the reason is familiarity or
something similar done recently. Naming that is useful, not embarrassing.

**Step 2. Generate three or more genuine alternatives.** Genuine is the requirement. Variations
on one approach are not alternatives, and neither is a straw option included so the preferred
one wins. Include at least one that differs in kind rather than degree, and where it applies,
include the option of doing nothing or doing the smallest possible version.

**Step 3. Compare on the same axes.** Pick axes that matter for this decision and hold them
across every option. Usually some of:

- effort to build, and effort to maintain, which are different numbers
- how it fails, and how loudly
- what it commits the team to later
- what the team already knows
- how it behaves at ten times the current load
- what it costs to reverse

**Step 4. Say what would change the answer.** For each option, the condition under which it
becomes the right one. This is what makes the comparison reusable when constraints shift.

**Step 5. Name what is not known.** The places where the comparison rests on assumption rather
than evidence, and what research would settle each. These become the research time.

**Step 6. Give a recommendation and its strongest counterargument.** Both. A recommendation
presented without its best objection has not been tested.

## Research time belongs in the estimate

This work takes time, and that time goes into the estimate explicitly rather than being absorbed
silently. Two related habits from the same section of the book:

- **Working hours and the deadline are different numbers.** Working hours are how long an
  undistracted engineer takes. The deadline is how many days from now it will be done,
  including waiting for prioritization and review.
- **Multiply the estimate by three.** Technology is finicky and unknown unknowns are reliable.
  Coming in early and picking up the next thing is better than being consistently late.

Optimism sounds good in the moment and costs credibility later. A manager hears "this will be
easy" and builds a deadline on it.

## Prompt the reader can run directly

> You are a senior engineer reviewing a design decision. The problem is [PROBLEM]. My first
> solution is [SOLUTION], and I picked it because [REASON].
>
> Give me at least three genuine alternatives, including one that is different in kind rather
> than a variation, and the smallest possible version if that is viable. Do not include options
> you do not consider real.
>
> Compare all of them, including mine, on the same axes: effort to build, effort to maintain,
> how it fails, what it commits us to later, and what it costs to reverse.
>
> For each option, tell me what would have to be true for it to become the right choice.
>
> Then tell me where this comparison rests on assumptions rather than evidence, and what
> research would settle each one.
>
> Finally, recommend one and give me the strongest argument against your own recommendation.

## What to tell the reader

- **The first idea often wins, and that is fine.** The value is in knowing why it won.
- **Put research time in the estimate.** Work that is not estimated is work that makes someone
  look slow.
- **Check the tool's confidence.** A fluent, assured answer is not evidence. Ask what it ruled
  out and why.
- **Keep the comparison.** It answers "why did we build it this way" a year later, and it is
  most of a design document already.

## What this skill does not do

It does not make the decision, know the team's constraints, or do the research it identifies.
It widens the field and makes the tradeoffs explicit enough to argue about.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

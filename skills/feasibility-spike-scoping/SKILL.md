---
name: feasibility-spike-scoping
description: Scope a time-boxed research spike for a capability nobody is sure is buildable yet, listing the current options with their maturity, stating what the spike must produce to support a go or no-go call, and naming what will need rechecking later. Use when someone is unsure whether a feature is technically possible, needs to size an unknown before committing to a roadmap, or is adding research time to a sprint.
---

# SKILL: Feasibility Spike Scoping

**From:** User Delight

## When to load this skill

Load this skill when the reader wants to promise something they are not sure can be built. The
specific case the book describes is a lead engineer who cannot say whether a capability belongs
in the release, because the tooling in that area moves faster than anyone can track.

That is the honest position, and a spike is what turns it into a decision rather than a guess.

## Why the spike exists

Two reasons, and both belong in the output.

**Nobody can keep every new tool top of mind.** In a fast-moving area, not knowing whether
something is possible is a statement about the pace of the field, not about the engineer. A
spike is the normal response.

**Even a rejected option teaches you something.** If the reader investigates an integration and
turns it down, they have still learned what the user values and what they would pay for. The
spike is not wasted when the answer is no, and framing it that way makes it much easier to
approve.

## What this skill produces

**A time box.** A concrete number of days, with the reasoning. Long enough to reach an answer,
short enough that it cannot quietly become the project.

**The current options with their maturity,** which is what distinguishes this from general
research. For each: what it does, how long it has existed, whether the interface is stable,
what it costs at the reader's expected volume, and what happens if the vendor disappears.

**The question the spike answers,** stated as one sentence. A spike without a question becomes
reading.

**What the spike must produce to support a go or no-go call.** Concretely: a working prototype
of the riskiest part, a cost figure at expected volume, a measured latency, a sample of output
quality against real inputs. Name which of these matter for this decision and which do not.

**What is out of scope.** The parts to deliberately not investigate yet, so the spike does not
expand into building the feature.

**What will need rechecking later.** In a fast-moving area, a finding has a shelf life. Say
which conclusions are durable and which should be revisited before the work actually starts.

**What a no teaches.** Spell it out in advance. It is what makes the spike worth funding.

## Write it down

Whatever the spike concludes, the reasoning goes in a memo: what the problem was, where the
research happened, what the options were, and what decided it. Management wants to see the
research, and more usefully, someone in a year will want to know why this choice was made.
Include that memo as a deliverable of the spike rather than an afterthought.

## Prompt the reader can run directly

> You are a lead engineer scoping a research spike. We want to build [CAPABILITY] as part of
> [PRODUCT], and I do not know whether it is technically feasible at our scale and budget.
>
> Scope a time-boxed spike. Tell me how many days and why.
>
> List the options that currently exist for this, and for each one: what it does, how mature and
> stable it is, what it costs at [EXPECTED VOLUME], and what the risk is if the vendor changes
> or disappears.
>
> State the one question this spike has to answer, and exactly what it must produce for me to
> make a go or no-go call.
>
> Tell me what to deliberately leave out of scope, and which findings will need rechecking
> before we build rather than now.
>
> Finally, tell me what we learn if the answer turns out to be no.

## What to tell the reader

- **A spike is not the feature.** The moment it starts producing something shippable, the time
  box has failed.
- **Cost at real volume, not at demo volume.** A capability that works in a demo and costs too
  much in production is a no that arrives late.
- **A no is a result.** It closes a question, and it tells you what the user actually wanted
  underneath the feature they asked for.
- **Put research time in the estimate.** Anything requiring a big decision deserves the room to
  make it on data.

## What this skill does not do

It does not run the spike, build a prototype, or produce real cost figures. It scopes the work
and defines what would count as an answer.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

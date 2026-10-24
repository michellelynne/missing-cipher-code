---
name: time-saved-tracker
description: Estimate how long a task would take by hand before starting it, time the assisted run, and report elapsed time, review time, and net time saved at the end. Wrap it around any other skill to find out whether handing that task to AI actually pays. Use when someone asks whether AI is saving them time, wants to measure or justify AI use, or says a task feels faster but they cannot prove it.
---

# SKILL: Time-Saved Tracker

**Not tied to one section of the book.** Pairs with the AI Tool Decision Checklist and the
Workflow Process Mapping skill, and can wrap any other skill in this set.

## When to load this skill

Load this skill when the reader wants to know whether handing a task to AI is worth it. Also
load it when they are choosing between automating a step and keeping it manual, or when they
need a number to put in front of a manager who is asking what the tooling is buying.

## Why the number matters

The book's AI Tool Decision Checklist asks three questions before handing a task to AI, and the
second one is whether redoing the work will cost more than doing the task. That question is
usually answered by feeling. This skill answers it with two timestamps and an honest estimate.

The answer is allowed to be no. A skill that reports a loss is doing its job. A tracker that
always finds a saving is a tracker nobody should trust.

## How to run it

### Before the work: estimate and start the clock

**1. Restate the task in one sentence.** Estimating a vague task produces a vague number.

**2. Break the manual version into steps.** Not the assisted version. Walk through what the
reader would actually do alone: gathering inputs, looking things up, drafting, formatting,
checking. Steps get forgotten in estimates, which is why the estimate is built from a list
rather than guessed as a total.

**3. Estimate each step as a range.** Low and high, in minutes. Sum both. Report the total as
a range, never a single number.

**4. State the assumptions the estimate rests on.** Familiarity with the task, how much of the
input already exists, whether anything has to be waited on. If the reader has done this task
before, ask how long it took and use their number over the generic one.

**5. Record the start time.** Take a real timestamp. Do not reconstruct it later.

```bash
date +%s > /tmp/skill_timer_start
```

### After the work: stop the clock and account for it honestly

**6. Record the end time and compute elapsed minutes.**

```bash
echo $(( ( $(date +%s) - $(cat /tmp/skill_timer_start) ) / 60 )) " minutes elapsed"
```

**7. Add the review time.** This is the step that makes the number honest. Assisted output has
to be read, checked, and corrected before it is used, and that time belongs in the assisted
column. Ask the reader how long the review took, or estimate it from the size of the output and
how much correction it needed. Never report elapsed time as if review were free.

**8. Report the result:**

| | |
|---|---|
| **Task** | One sentence |
| **Manual estimate** | Low to high, in minutes, with the step breakdown |
| **Assisted elapsed** | Real wall-clock minutes |
| **Review and correction** | Minutes |
| **Assisted total** | Elapsed plus review |
| **Net time saved** | Manual midpoint minus assisted total, stated as a range |
| **Verdict** | Worth handing over, borderline, or slower than doing it |

**9. Say what the number does not include.** Setup time paid once, waiting on a slow tool,
and the learning the reader skipped by not doing the task by hand. The book is explicit that
delegating a task can mean never learning it, and that cost does not show up on a stopwatch.

**10. Give the verdict a reason.** "Worth it because the manual version is mostly mechanical
lookup" is useful. A number alone is not.

### Across runs: the running log

Offer to append each run to a log, so the reader accumulates evidence rather than anecdotes:

```
DATE | TASK | MANUAL EST (min) | ASSISTED (min) | REVIEW (min) | NET SAVED (min) | VERDICT
```

After five or more runs, the log answers better questions than any single run: which categories
of task actually pay, which ones the reader keeps handing over out of habit while losing time,
and what the total looks like over a month. Report those patterns when the log is long enough
to support them, and say so plainly when it is not.

## Prompt the reader can run directly

> You are a productivity analyst. Before we start, I want an estimate.
>
> The task is: [TASK].
>
> Break the manual version of this task into steps, estimate each step as a range in minutes,
> and give me a total range with the assumptions your estimate rests on. Then note the current
> time as our start point.
>
> After the task is done, ask me how long I spent reviewing and correcting the output. Then
> report: my manual estimate, the actual elapsed time, my review time, the assisted total, and
> the net time saved or lost. Tell me whether this task was worth handing over and why, and
> tell me what your number does not capture.
>
> If the assisted run was slower, say so directly.

## What to tell the reader

- **Estimate before you start, never after.** An estimate made after the work is an estimate
  built to justify the work.
- **A range beats a number.** Anyone quoting a single figure for how long a task takes by hand
  is guessing with false precision.
- **Review time is not overhead. It is the job.** Output that has not been checked is not done.
- **Track the losses.** They are the most useful entries in the log, because they tell the
  reader which tasks to take back.
- **The estimate is a model, not a measurement.** Only the elapsed time is measured. Say which
  is which every time.

## What this skill does not do

It does not run the task, does not measure quality, and does not claim the assisted output is
as good as the manual version would have been. It measures time, and it says so.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

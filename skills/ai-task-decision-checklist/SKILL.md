---
name: ai-task-decision-checklist
description: Walk the three questions that decide whether to hand a task to AI (whether it can do the task well, whether redoing its work costs more than doing it yourself, and whether a secure tool is actually available), then say which kind of no you are dealing with. Use when someone is deciding whether to automate a task, wondering if an AI tool is worth it, or has been told a tool is not available at their company.
---

# SKILL: AI Tool Decision Checklist

**From:** Index Card Design Worksheet

## When to load this skill

Load this skill when the reader is deciding whether a task should go to AI. Also load it when
they have been told a tool is unavailable and are not sure whether that is the end of it.

## The three questions

Ask all three. A no on any one of them is a no overall, but for different reasons and with
different remedies.

**1. Can it complete the task well?**

Be specific about this task rather than the category. Judge against what the reader would
produce, not against perfection. Consider whether the task has a verifiable right answer, how
much context it needs that lives only in the reader's head, and whether a plausible-looking
wrong answer would be spotted or shipped. The last one is the real risk: tasks where wrong
output is obvious are safe to delegate; tasks where wrong output looks fine are not.

**2. Will the reader spend more time redoing its work than doing the task themselves?**

This is the question people answer by feeling. Push for an estimate: how long the task takes by
hand, how long the assisted version takes, and how long the review takes. Review time counts.
If the reader wants this measured rather than guessed, the time-saved-tracker skill does exactly
that and this checklist pairs with it.

**3. Is there a secure tool available at the organization?**

Availability and permission are different things, and this question is about both.

**On the third question, find out which kind of no it is.** The book is explicit that this is
worth researching rather than assuming:

- **Nobody asked.** A request may be all it takes, though approval takes time. Worth starting
  now even if the current task moves on without it.
- **Security or legal blocked it.** That is the answer, and the reader should stop looking for
  a way around it. This is the case where using a personal account for work material creates a
  real problem for them rather than a technicality.

Do not let the reader treat an unanswered question as a blocked one, and do not let them treat
a blocked one as an unanswered one.

## What this skill produces

A short verdict with the reasoning visible:

| | |
|---|---|
| **Task** | One sentence |
| **Can it do it well** | Yes, no, or partly, with what it would get wrong |
| **Redo cost** | The comparison, with review time counted |
| **Tool available** | Yes, no because nobody asked, no because it is blocked, or unknown |
| **Verdict** | Delegate, delegate with review, split, or keep |
| **If unknown** | The specific question to ask, and whom to ask |

"Split" is often the right answer and gets overlooked. Many tasks divide into a mechanical part
worth delegating and a judgment part worth keeping.

## Prompt the reader can run directly

> You are helping me decide whether to hand a task to AI. The task is [TASK]. I would do it by
> [HOW YOU DO IT NOW], and it takes about [TIME].
>
> Walk me through three questions. First, could AI do this task well, and specifically what
> would it get wrong? Second, would I spend more time reviewing and redoing its work than just
> doing it, counting review time honestly? Third, what would I need from a secure tool at my
> company to do this safely?
>
> Then give me a verdict: delegate, delegate with review, split the task, or keep it. If the
> answer depends on something I have not told you, say what you need to know.
>
> If part of this task is mechanical and part needs my judgment, say where the line is.

## What to tell the reader

- **The answer is allowed to be no.** A checklist that always says delegate is not a checklist.
- **Ask about the tool before assuming.** The difference between "nobody asked" and "legal said
  no" is the difference between a request and a policy violation.
- **Never route around a blocked tool.** Pasting work material into a personal account because
  the company tool was refused is the exact outcome the block exists to prevent.
- **Recheck occasionally.** What the tools can do and what the organization allows both change,
  and a no from last year is not evidence today.

## What this skill does not do

It does not perform the task, measure the time, or know the organization's policy. It structures
the decision and names what the reader still has to find out.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

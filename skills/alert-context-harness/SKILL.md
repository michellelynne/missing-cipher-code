---
name: alert-context-harness
description: Build the context package an assistant needs before it can write useful alerts or tests, carrying the user workflows, personas, and what counts as broken from the user's side, then check existing alerts against whether a user would actually notice. Use when automated alerts keep missing real incidents, when AI-written tests and alerts only reflect the code, or when someone is setting up alerting for a service.
---

# SKILL: Alert Context Harness

**From:** User Experience Alerts

## When to load this skill

Load this skill when alerts are firing for things nobody cares about, missing things everyone
cares about, or when the reader is about to ask a tool to write alerts and wants the result to be
worth keeping.

## The diagnosis

An assistant with only the code in front of it cannot tell you what users are doing. So it writes
tests and alerts against what the code does, and then an incident happens and the alerts miss it.

The model is not the problem. It is missing context. Nobody would hire an engineer, skip the demo
of what the product is supposed to do, and send them off to fix things. The same courtesy applies
here, and on a project the reader works on regularly it is worth spending the time once to build
the context properly.

That context package is what this skill produces.

## What goes in the harness

**The personas.** Who uses this, what they are trying to accomplish, and how their use differs.
A contractor on a phone at a job site and an admin at a desk fail in different ways.

**The workflows.** The actual journeys, end to end, in order. What a user does first, what they
do next, and what they are waiting on at each step.

**What broken means, per workflow.** Stated from the user's side. Not "the endpoint returns 500"
but "the homeowner cannot submit their quiz." These are different events and only the second one
is worth waking someone for.

**What is merely annoying.** If the user can still finish the workflow, it is a feature request,
not an alert. Drawing this line in advance prevents most alert sprawl.

**The blast radius.** Which workflows a given service failing actually blocks, which is usually
narrower or wider than the team assumes.

## The test every alert must pass

Finish this sentence: *this alert is being set up because otherwise [some bad outcome to the
user]*. An alert that cannot complete it is measuring a cause rather than a symptom, and belongs
on a dashboard instead of in a pager.

The related trap is threshold theater. Eighty percent CPU sounds like a sensible alert until you
notice that users suffer at fifty, or never notice at ninety-nine, or that an autoscaler is keyed
to that number and handles it. Rate of change often matters more than the level: a disk at fifty
percent filling fast is an emergency; one at ninety percent filling slowly is next week's ticket.

## What this skill produces

1. **The context package,** in a form that can be pasted in or saved as a reusable skill.
2. **A review of existing alerts** against the completion test, sorted into the ones a user would
   notice and the ones they would not.
3. **The gaps:** workflows with no alert covering them, which is the category that produces the
   incident nobody saw coming.

## Prompt the reader can run directly

> I want to build a reusable context package before we write any alerts.
>
> Our product is [PRODUCT]. The personas are [PERSONAS]. Here are the main user workflows:
> [WORKFLOWS]. Here is the service map: [SERVICES AND WHAT THEY DO].
>
> For each workflow, write down what "broken" means from the user's point of view, what would be
> merely annoying rather than broken, and which services failing would block it.
>
> Then review my existing alerts: [ALERTS]. For each, complete the sentence "this alert is being
> set up because otherwise ___ happens to the user." Flag every one that cannot complete it.
>
> Finally, tell me which user workflows have no alert covering them at all.

## What to tell the reader

- **Build the harness once, reuse it.** On a project worked on often, this is the highest-leverage
  thing to write down, and it improves tests and documentation too.
- **More context helps everyone.** The same package that fixes AI output also onboards new
  engineers and contractors faster.
- **Symptom over cause.** Alert on what the user experiences; put the causes on a dashboard for
  whoever is already investigating.
- **Noisy alerts are worse than none.** They train people to ignore the pager.

## What this skill does not do

It does not configure alerting, set thresholds, or connect to a monitoring platform. It builds
the context that makes the resulting alerts worth having.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

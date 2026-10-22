---
name: api-log-questions
description: Answer plain-language questions about API usage logs directly, returning the answer plus the underlying data, instead of designing a new dashboard for every question that comes up once. Use when someone wants to know how an API is actually being used, who is on which version, or whether a change is safe to make, and does not want to build a chart to find out.
---

# SKILL: API Log Questions

**From:** API Dependability

## When to load this skill

Load this skill when the reader has a question about how their API is being used and the honest
answer is that nobody knows. Also load it when they are about to build a dashboard for a question
that may never come up again.

## Why this beats a dashboard

Dashboards are good at questions you knew you would have. They are bad at the question you have
right now, because answering it means designing a new chart, and the cost of that design work
means the question often just goes unanswered.

Asking in plain language removes that cost. The tradeoff is that a dashboard is repeatable and an
answer is not, so recurring questions should still graduate into a dashboard once they have
proven recurring. The reader is not choosing one or the other.

## Why this matters for an API specifically

When an API is released, it gets used in ways nobody anticipated. The standard way to discover
those ways is to ship a breaking change and wait for the complaints, which is an expensive
research method. Usage logs are the cheap version.

So the first move after release is to track all usage, so that questions about it have somewhere
to land.

## Questions this handles well

- Which endpoints get the most traffic, and from whom
- Which are barely used, and by whom specifically, because that is who a deprecation affects
- Which clients are on which version, and how a migration is progressing
- Which endpoints error most, and whether that is concentrated in one caller
- What usage looked like before and after a change
- Whether anyone actually uses the parameter about to be removed

## What this skill returns

**A direct answer first,** in one or two sentences.

**Then the underlying data,** because the answer alone is not checkable. The reader needs to see
the rows, the counts, or the query that produced them.

**Then the caveats:** what the logs do not capture, what time range this covers, and whether
anything looks like it is missing rather than absent. A caller that stopped appearing may have
stopped calling or may have stopped being logged.

## Prompt the reader can run directly

> You have access to my API usage logs at [SOURCE]. The schema is [SCHEMA, OR "please inspect
> it"].
>
> Answer this question: [QUESTION IN PLAIN LANGUAGE].
>
> Give me the direct answer first, then the data behind it and the query you used. Then tell me
> what these logs do not capture that would change the answer.
>
> If the logs cannot answer this, say so rather than approximating.

## What to tell the reader

- **Check the query, not just the answer.** A confident wrong answer from a subtly wrong filter
  looks exactly like a right one.
- **Absence is ambiguous.** No log lines can mean no usage or no logging, and those lead to
  opposite decisions about a deprecation.
- **Promote recurring questions.** A question asked three times deserves a dashboard.
- **This does not replace versioning.** Knowing who uses what is the input to a change management
  plan, not a substitute for one.

## What this skill does not do

It does not instrument the API, decide whether a change is safe, or notify anyone. It answers
questions from logs that already exist and shows its working.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

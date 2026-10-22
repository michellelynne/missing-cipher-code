---
name: documentation-drafting
description: Draft documentation for a service or feature organized around who, what, where, when, why and how, ordered most important first, then require an edit pass that cuts a meaningful share of it before publishing. Use when someone needs to document a system, is writing a README or handover doc, or has generated documentation that is technically complete and unreadable.
---

# SKILL: Documentation Drafting

**From:** Documentation

## When to load this skill

Load this skill when the reader has to document something and does not know where to start, or
when what they have is a stream of everything they know rather than something a reader can use.

## Who this is for

Documentation is written to someone in the future. That person is the whole audience, and they are
the one both common failure modes forget.

Engineers tend to write down everything they know in the order they thought of it. Generated
documentation tends toward length, because verbosity is not penalized and in many pricing models
is literally what is billed. Neither style accounts for the person who has to read it.

Knowing that the incentive runs toward length is useful, because it means the correction has to be
deliberate: ask for concision explicitly, set a length limit, and cut afterward.

## The structure

Six questions, from journalism, where they exist to make sure a story covers everything essential.

**Who was involved?**
- Who developed this originally?
- Who can I contact with development questions?
- Who can I contact for user support?
- Who are the personas this was developed to serve?
- Who do you inform of new updates?

**What happened?**
- What was the original problem?
- What is the main goal of the product?
- What are all the workflows and features?
- What operational tools are available to support it?
- What is the current service level agreement?

**Where did it take place?**
- Where are all the technical pieces: repositories, build pipelines, logs, test suites, external
  configuration?

**When did it happen?**
- When was it originally developed, and what was the timeline?
- Was it rushed, or developed with more lax deadlines?
- When was the latest update?

**Why did it happen?**
- Why was this the solution chosen?
- Why were other solutions not used?
- Why did the developers make these technical choices?

**How did it happen?**
- How does the system work?
- How do you install it?
- How do you build and test locally?
- How do you deploy and run all the tests?
- How is it being used today?
- How does new user onboarding work?

These are a starting point. Not all of them need answering, and the list is not a limit.

## Order by importance, not by the list

Engineers skim. Like a resume, the most important information goes at the top, and which
information is most important depends on the organization, the team, and the product. Some
questions have standard answers across every service at a company and can be dropped entirely.

## The required edit pass

The draft is not the deliverable. Before publishing:

- Cut a meaningful share of it. Expect to lose a third and lose nothing of substance.
- Delete every sentence that explains what the next section will explain.
- Replace anything vague with the specific thing.
- Read it as someone who has never seen this system.

**Pair with someone fresh to the service.** They will ask the questions and find the gaps, which
is the single most effective review available.

## Prompt the reader can run directly

> You are a technical writer. I need documentation for [SERVICE OR FEATURE]. Here is what I know:
> [PASTE NOTES, CODE, OR BOTH].
>
> Organize it around who, what, where, when, why, and how, using only the questions that apply.
> Put the most important information first for a reader who is [WHO WILL READ THIS].
>
> Be concise. Do not write introductory sentences that describe what a section will say. Keep it
> under [LENGTH].
>
> Then tell me which questions you could not answer from what I gave you, and flag anything you
> inferred rather than knew.

Then, before publishing:

> Now cut this by a third without losing any substance. Show me what you removed.

## What to tell the reader

- **Read and verify every word.** Documentation is trusted because someone checked it. The last
  place anyone wants an invented detail is the document people follow during an incident.
- **Ask for brevity explicitly.** The default runs long, and knowing why makes it easier to
  correct.
- **Flag inferences.** Anything assembled from code rather than known is a question for a person.
- **Do not duplicate.** Link back to the source of truth rather than restating it, or the copies
  will disagree within a quarter.

## What this skill does not do

It does not verify the system works as described, publish anything, or know the organizational
context that only a person has. It produces a structured draft that still needs cutting.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

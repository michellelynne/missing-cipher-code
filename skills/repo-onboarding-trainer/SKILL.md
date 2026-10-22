---
name: repo-onboarding-trainer
description: Walk someone through an unfamiliar repository pitched at the experience they actually have, covering how the connected repos fit together to produce the product, then how to bring up a local environment, run the tests, and deploy a change, with unlimited repeat questions. Use when someone joins a team, inherits a service, has to work in a repo they have never seen, or found the documentation written for someone who already knows it.
---

# SKILL: Repo Onboarding Trainer

**From:** Senior Backend Engineer to Fullstack Engineer (AI as a Custom Trainer)

## When to load this skill

Load this skill when the reader faces a repository they do not know. New job, new team, an
inherited service, or a codebase everyone else has context on.

## The problem this solves

Everyone who writes documentation thinks it is clear. Everyone who reads it thinks it is in
another language. The cause is structural: the person documenting cannot know what the reader
already knows, and consistently overestimates it.

This skill inverts that. The reader states their actual background, and the walkthrough is
pitched there. A backend engineer who has never opened a frontend repo needs something
different from a new graduate, and both need something different from what the README assumes.

The second advantage matters as much and gets discussed less. The reader can ask the same
question five times without it costing them anything socially. That is not true of asking a
teammate, and it is the reason people stay confused longer than they need to.

## Required inputs

1. **The repository,** or enough of it to work from.
2. **The reader's background.** Languages they know, stacks they have worked in, years of
   experience, and what they already understand about the product. Specific beats modest here.
3. **What they have already used.** Someone who has used the product knows how it behaves and
   only needs the mapping from behavior to code.

## What this skill produces

Layered, in this order. Do not skip ahead to the code.

**1. What this repo is for,** in the reader's own terms, and where it sits relative to the
other repos that make up the product.

**2. How the connected repos fit together.** Very few repos are independent. Which repo owns
what, which calls which, where the data comes from, and what has to be running for this one to
work. This is the layer documentation almost always omits, because the person writing it
absorbed the answer months ago.

**3. The map of this repo.** The directories that matter, what lives in each, where a request
or interaction enters, and the path it takes through. Skip the directories nobody touches and
say that is what you are doing.

**4. Local environment.** Every step to get it running, including the ones considered obvious.
The obvious ones are where people get stuck.

**5. Running the tests.** How to run all of them, how to run one, and how long to expect.

**6. Deploying a change.** The path from a local edit to running code: branch conventions,
review requirements, what runs automatically, and what a person has to do.

**7. A first safe change.** Something small and low-risk that exercises the whole loop. Getting
one trivial change all the way through is worth more than reading for a day.

## Follow-up mode

After the walkthrough, stay available for repeat questions and answer them as if asked for the
first time. Never reference having already explained something. That reaction is exactly what
makes people stop asking, and it is the specific advantage this has over a colleague.

## Prompt the reader can run directly

> You are a senior [STACK] engineer onboarding a new teammate. I am a [YOUR BACKGROUND]
> engineer who has never seen this repository. I have used the product and understand how it
> behaves.
>
> Walk me through this repo and the repos connected to it, explaining how the systems fit
> together to produce [THE PRODUCT OR UI]. Then show me how to bring up a local environment,
> run the tests, and deploy a change.
>
> Pitch it at my background. Assume I know [WHAT YOU KNOW] and do not assume I know anything
> about [WHAT YOU DO NOT].

Then keep asking. Repeat questions are the point.

## What to tell the reader

- **State your background honestly.** Overstating it produces a walkthrough that skips the part
  the reader needed.
- **Verify the connections.** How repos fit together is the layer most likely to be inferred
  rather than known, and the most expensive to get wrong.
- **Code says what, not why.** The business reason a piece of code exists is usually nowhere in
  the repository. That question goes to a person.
- **Do the first small change early.** It surfaces every broken assumption in the setup at once.

## What this skill does not do

It does not grant access, run anything, or know the team's undocumented decisions. It produces
a walkthrough pitched at the reader instead of at whoever wrote the README.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

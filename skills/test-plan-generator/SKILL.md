---
name: test-plan-generator
description: Design a test plan before any code is written, starting from what users do, working through the five test families, and recommending a manual-first then automated ordering, framed as the start of a conversation with QA rather than a replacement for one. Use when someone gets a feature request, is planning tests, works without a dedicated QA engineer, or has a test suite that is large and still missing things.
---

# SKILL: Test Plan Generator

**From:** Tests, Tests, and More Tests

## When to load this skill

Load this skill when a feature request arrives and before any code is written. That timing is the
point. A test plan produced afterward documents what was built rather than checking whether it is
right.

## The failure mode this replaces

Two versions of it, and both are common. In one, the reader asks an assistant for the feature,
then asks it for tests, and gets so many that nobody reads them, so they ship. In the other, the
reader writes the feature and adds one or two unit tests, and ships. The first bloats the
repository, the second catches almost nothing, and neither is comprehensive.

The alternative is to design the plan first, from the user's actions, and make it part of the
ticket before coding starts. In a well-resourced team that is a conversation with a QA engineer.
This skill is what to do when that person does not exist, or the preparation for talking to them
when they do.

## Start with the questions QA would ask

- Is this a frontend or backend feature?
- How would users typically use this feature?
- If backend, is it backward-compatible for anyone using the API?
- Is there a command-line interface that also needs testing?
- If frontend, which pages does it affect?
- Does it appear in one place, or is it a repeated element?
- What user interaction is possible but will result in an error?
- Are the error messages clear and actionable?
- Are there current manual or automated tests this feature could affect?
- What is the current test coverage for this area?

Answer these before proposing a single test. They are what turn a feature description into a
testable surface.

## The five families

| Family | The question it answers |
|---|---|
| **Functional** | Does the product do what it is supposed to do? |
| **Non-functional** | How well does it do that, and for whom? |
| **Structural and code level** | How good is the code itself and its test coverage? |
| **Infrastructure and reliability** | What happens when there is a problem with the infrastructure? |
| **Process-oriented** | How do you test with real users and real traffic? |

Work each family in turn. Most plans written without a framework land entirely in the first and
third, which is how a suite ends up large and still surprised by an outage.

## Manual first, then automate

Start with manual tests that match the user's actions, then automate them.

Automating too early is like abstracting too early. It makes everything harder to change and
guarantees missed coverage, because the reader automates their assumptions before finding out
which ones were wrong.

So the plan is ordered: what to check by hand first, what to automate once it is stable, and what
should stay manual permanently.

## Find the balance

Under-test and every release introduces bugs. Over-test and the suite takes too long to run, which
leads to people skipping it, which is under-testing with extra steps. The target is a suite where
anyone on the team can change the application with confidence because the right tests always run.

## Prompt the reader can run directly

> You are a QA engineer helping me design a test plan before I write any code.
>
> The feature is: [DESCRIPTION]. The user-facing behavior is: [WHAT THE USER DOES AND SEES]. It
> affects [FRONTEND / BACKEND / BOTH], specifically [PAGES OR ENDPOINTS]. Current coverage in this
> area is [WHAT EXISTS].
>
> First ask me anything you need to know that I have not told you.
>
> Then give me a test plan organized by functional, non-functional, structural and code level,
> infrastructure and reliability, and process-oriented testing. For each test, say what
> user-facing outcome it protects.
>
> Recommend which to do manually first, which to automate once stable, and which should stay
> manual. Flag any existing tests this feature could break.

## What to tell the reader

- **This is the start of a conversation, not a replacement for one.** If a QA engineer exists,
  bring this to them rather than instead of them.
- **Put the plan in the ticket.** A plan agreed before coding is a shared definition of done.
- **Count what it protects, not how many there are.** Suite size is not a quality metric.
- **Error messages are part of the feature.** Whether they are clear and actionable is testable.

## What this skill does not do

It does not write or run tests, measure coverage, or decide what ships. It designs the plan while
it can still influence the code.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: migration-tdd-scaffolding
description: Write the test case plan before any implementation for a feature being extracted into a new service, covering the happy path, the failure cases named, and the ones missed, with each test stating in one line what user-facing outcome it protects. Use when someone is scaffolding a new service, extracting a feature whose expected behavior is already known, or wants tests that check user outcomes rather than function behavior.
---

# SKILL: Migration TDD Scaffolding

**From:** Migrating a Legacy System

## When to load this skill

Load this skill when the reader is building a service to replace something that already works.
That is the ideal case for test-first development, because the expected behavior is not a guess:
the old system is the specification.

## Why tests come first here

The reader already knows exactly how this feature should behave and what it should output.
Writing the tests before the implementation turns that knowledge into an executable definition of
done, and it catches the places where the old behavior is not what anyone assumed.

## The failure mode to avoid

It is tempting to ask for all the tests at once and accept what comes back. The result tends to
be a large suite that verifies functions work as written rather than that users get what they
need. Those are different claims, and only the second one matters.

So every test carries one line saying **what user-facing outcome it protects**. A test that
cannot answer that is testing an implementation detail, and it will break on the first refactor
while catching nothing.

## What this skill produces

**The test case plan, before any implementation:**

- **Happy path.** The main flow, from the user's point of view.
- **The failure cases the reader named.**
- **The failure cases they did not.** This is where the value is. Missing inputs, partial data,
  the downstream service being down, the same request arriving twice.
- **Edge cases and unexpected data.** Empty, enormous, malformed, wrong encoding, wrong type.
- **Resilience cases.** What happens under retry, timeout, and partial failure.

Each test labeled with which scenario it belongs to, so the suite reads as a map of the behavior
rather than a list.

**Then the scaffolding:** project structure with the test stubs in place, ready for the
implementation to fill in.

## Ground it in the user

Before generating anything, state the behavior from the user's point of view rather than the
system's. "The homeowner gets one notification when all their images finish" is testable against
what the user experiences. "The notification service fires on queue drain" is testable against
what the code does, and those can both be true while the user gets nothing.

## Prompt the reader can run directly

> You are a test engineer. Here is the behavior this feature must produce, described from the
> user's point of view: [BEHAVIOR].
>
> Write the test case plan before any implementation. Cover the happy path, these failure cases
> I already know about: [FAILURES], and any cases I did not think of. For each test, state in one
> line what user-facing outcome it protects.
>
> Then make a plan for edge cases and unexpected data or failures, and any other tests that would
> make this more resilient. Make it clear which test case is for which scenario.

## Package it as a harness

If more than one person will work on this migration, the context is worth packaging so everyone
starts from the same conventions. Adding structure around an agent keeps it on task and reduces
invention, and the simplest version of that structure is a skill, which works across tools and
models. Once the plan is settled, the reader can ask for a skill version of it so the next
engineer inherits the approach rather than reinventing it.

## What to tell the reader

- **Be clear in your direction and check the work.** Grounded instructions plus review is the
  whole technique.
- **A passing suite is not a working feature.** It means the behavior you described is protected.
  Whether you described the right behavior is still on you.
- **The old system is your oracle.** When a test's expected value is unclear, go and observe what
  the current system actually does rather than deciding what it should do.

## What this skill does not do

It does not write the implementation, run the tests, or confirm the extracted feature matches the
original. It turns known behavior into a test plan and a scaffold.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

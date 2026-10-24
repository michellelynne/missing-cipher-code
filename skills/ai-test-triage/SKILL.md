---
name: ai-test-triage
description: Triage an AI-generated test suite by grouping the tests by what they actually verify, flagging duplicates and tests that check framework or implementation behavior rather than product behavior, and returning a shortlist worth keeping with the reason for every cut. Use when AI wrote more tests than anyone can read, when a suite is bloated or slow, when reviewing a pull request full of generated tests, or when someone asks which tests actually matter.
---

# SKILL: AI Test Triage

**From:** Tests, Tests, and More Tests

## When to load this skill

Load this skill when the tests came from an assistant and there are too many to read. You ask AI
to write the tests, it writes so many that your eyes glaze over, and you push. That catches some
problems, but it may just be bloating the repository.

The goal is the right tests, the ones that give real confidence, so anyone can change the app
without fear. Under-test and every release creates new bugs. Over-test and the suite takes too
long to run, and nobody reads the failures.

## The test that every test has to pass

**What would break for a user if this test were deleted?** A test with a clear answer stays. A
test whose only answer is "a function would behave differently from how it was written" is
checking the implementation, not the product.

## How to run it

1. **Get the feature** the tests cover, described from the user's point of view, and the suite.
2. **Group the tests by what they actually verify,** not by file or name. Generated test names are
   often misleading.
3. **Sort each group into the five test families** so gaps show up alongside the excess:

| Family | The question it answers |
|---|---|
| **Functional** | Does the product do what it is supposed to do? |
| **Non-functional** | How well does it do it, and for whom? |
| **Structural and code level** | How good is the code itself and its test coverage? |
| **Infrastructure and reliability** | What happens when there is a problem with the infrastructure? |
| **Process-oriented** | How does it behave with real users and real traffic? |

4. **Flag what to cut:**
   - **Duplicates,** several tests asserting the same behavior with different inputs that do not
     exercise anything new.
   - **Framework tests,** asserting that the language, library, or framework works.
   - **Mirror tests,** that restate the implementation line by line and will break on any refactor
     while catching nothing.
   - **Over-mocked tests,** where everything interesting is mocked away.
   - **Tests with no clear assertion,** or that pass no matter what.
5. **Flag what is missing.** Usually error cases, unclear error messages, backward compatibility
   for API consumers, and anything in a family with no tests at all.
6. **Return the shortlist,** each kept test with one line on the user outcome it protects, each cut
   with its reason, and the gaps.

## Prompt the reader can run directly

> Here is a feature, described from the user's point of view: [FEATURE]. Here is the test suite an
> AI assistant generated for it: [PASTE OR REPO PATH].
>
> Group the tests by what they actually verify, not by name. Sort them into functional,
> non-functional, structural and code level, infrastructure and reliability, and process-oriented
> tests. Flag duplicates, tests that check the framework or restate the implementation, tests that
> mock away the behavior that matters, and tests with no meaningful assertion.
>
> Give me a shortlist worth keeping, with one line each on the user-facing outcome it protects, and
> the reason for every test you would cut. Then tell me what is missing. Do not delete anything; I
> will decide.

## What to tell the reader

- **Test manually first,** using the user actions as a guide, then automate. Automating too soon is
  like abstracting too soon.
- **Bring in QA early.** If you have a QA engineer, the test plan belongs in the ticket before the
  code. Their questions are better than any generated suite.
- **Review before you delete.** A test that looks redundant sometimes guards a bug someone fixed
  once. Check the history.
- **Next time, plan first.** Asking for a test plan before the code (see `test-plan-generator`)
  produces fewer, better tests than asking for tests after.

## What this skill does not do

It does not delete tests, run the suite, or measure coverage. It tells you which tests earn their
place and why.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

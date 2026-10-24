---
name: design-round-exploration
description: Sketch a low-fidelity wireframe from a user story and call to action, then flag the accessibility, responsiveness, and edge-case problems worth resolving before anyone builds it, since a problem caught in a design round is far cheaper than one caught in code. Use when someone is designing a page or screen, working without a designer, preparing for a design review, or wants to check a layout before building.
---

# SKILL: AI-Assisted Design Exploration

**From:** Role of a Designer (Designer Workflow)

## When to load this skill

Load this skill when the reader needs to think through a screen before building it. That
includes engineers working without a designer, and engineers preparing to give a designer
useful feedback.

## Why the round matters

Design moves through stages, and each one costs more than the last:

1. **Rough sketches.** Whiteboard, notebook, index cards. Generating an idea should be as cheap
   as possible so a bad one can be thrown away without regret.
2. **Wireframes.** Boxes with labels. Sharper than a sketch, focused on flow rather than
   appearance. Reviewed by the people doing the work rather than by management.
3. **High-fidelity mockups.** Most of the application, with real type, color, and alignment.
   This is where accessibility, edge cases, and missing components get attention.
4. **Prototype.** A mockup that can be navigated. Nothing connects to a backend, but it is real
   enough to put in front of a stakeholder.

At any stage the work can go back a round, or back to the start. Since each artifact is harder
to produce than the one before it, anything caught early is money the organization does not
spend. Changing a wireframe is cheap. Changing a shipped page is not.

## Required inputs

1. **The user story** the page serves.
2. **The call to action.** One per page. If the reader names two, the first useful thing this
   skill can do is ask which one the page is actually for.
3. **Who uses it,** and on what. A contractor on a phone at a job site and an office worker on
   two monitors need different pages.
4. **What data the page has access to.**

## What this skill produces

**A low-fidelity wireframe described in words:** the regions of the page top to bottom, what
sits in each, what is a control and what is content, and where the call to action lives. Boxes
with labels, in prose. This is deliberately not a visual design.

**The states the page has to handle,** which is where most wireframes are thin: empty, loading,
partial data, error, and the state where there is far more data than the design assumed.

**Accessibility problems to resolve before building.** Contrast, anything signaled by color
alone, focus order, controls without labels, images without meaningful alternative text, and
whether the page still works at high zoom.

**Responsiveness problems.** What happens to this layout on a narrow screen, and which element
is the one that breaks first.

**Edge cases and missing components.** The long name, the empty list, the user with one item
and the user with four hundred, the permission that hides half the page.

**A short list of questions for a designer or the team,** where the answer is a judgment call
rather than a rule.

## Prompt the reader can run directly

> You are a senior product designer. I am designing a page for [PRODUCT]. The user story is
> [STORY]. The single call to action is [ACTION]. The user is [WHO] on [DEVICE]. The page has
> access to [DATA].
>
> Describe a low-fidelity wireframe: the regions of the page in order, what is in each, and
> where the call to action sits. Boxes with labels, not visual design.
>
> Then list the page states I need to handle, the accessibility issues I should resolve before
> building, what breaks on a narrow screen, and the edge cases this layout has not accounted
> for.
>
> Finally, give me the questions I should take to a designer, where the answer is a judgment
> call rather than a rule.

## What to tell the reader

- **One call to action per page.** A page asking for two things gets neither reliably.
- **A designer is still worth having.** This is a way to arrive at a design conversation with
  something to react to, not a replacement for the person who does this professionally.
- **Get feedback while it is cheap.** Wireframes are easy to change. That is the entire reason
  the stage exists.
- **Automated accessibility checks are a first pass.** They catch roughly half of what is
  there. The rest needs a person.

## What this skill does not do

It does not produce images, mockups, or design files, and it does not replace user research or
usability testing. It gets the reader to a reviewable wireframe with its problems already named.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: accessibility-screen-audit
description: Audit one screen's markup and styling against a named accessibility standard, returning each failure with its success criterion number, the exact element, one sentence on why it fails, and a suggested code change, ordered with the failures a screen reader user hits first. Use when someone is auditing a page for accessibility, has scanner output they need to act on, or wants a specific screen checked before it ships.
---

# SKILL: Accessibility Screen Audit

**From:** Accessibility Audit Worksheet (Accessibility Audit)

## When to load this skill

Load this skill when the reader has one screen to check. One at a time is the right granularity:
an audit of a whole application produces a list nobody works through, while an audit of a single
page produces tickets.

Know which standard and level applies before starting. The standards lookup skill covers that.

## What this skill produces

For every failure:

| Field | Content |
|---|---|
| **Success criterion** | The number, so it is checkable against the standard |
| **Element** | The exact element, not a description of where it roughly is |
| **Why it fails** | One sentence |
| **Suggested change** | The actual code, not the principle behind it |

**Ordered by who hits it first, starting with screen reader users.** A list ordered by severity in
the abstract is less useful than one ordered by how early in the experience it blocks someone.

## What to look at

The failures that cluster:

- **Contrast** below the required ratio, especially secondary text and text over images.
- **Colour as the only signal.** Status indicated purely by colour is invisible to a large number
  of users. Text or an icon has to carry it too.
- **Missing or empty alternative text** on images that carry meaning, and alternative text on
  images that do not.
- **Unlabelled controls.** Icon buttons with no accessible name are the standard offender.
- **Focus order** that does not follow the visual order, and focus that vanishes entirely.
- **Keyboard traps,** anywhere focus can enter and not leave.
- **Zoom and reflow.** Whether the page still works at high zoom without horizontal scrolling.
- **Headings** used for size rather than structure, which breaks navigation for anyone using
  headings to move around.
- **Form errors** that are shown visually but never announced.

## The limit that must be stated

**An automated pass is a first pass.** Scanners catch roughly half of what is there, which is a lot
and is not most.

They can tell you whether something is present. Only a person can say whether the page makes sense
to someone using a screen reader. A page can pass every automated check and still be incoherent to
navigate, because coherence is not a property any scanner tests for.

So the output ends with **what still needs manual review**, specifically: whether the reading order
tells a sensible story, whether the labels make sense out of context, whether an error message
explains what to do, and whether anyone has actually driven this page with a keyboard only.

Run more than one scanner if possible. They disagree, and the disagreements are findings.

## Prompt the reader can run directly

> You are a senior frontend engineer reviewing one screen for accessibility. Here is the markup and
> styling for [PAGE NAME]: [PASTE].
>
> Audit it against [STANDARD AND LEVEL].
>
> For each failure, give the success criterion number, the exact element, one sentence on why it
> fails, and a suggested code change. Put the failures a screen reader user would hit first.
>
> Then tell me what you cannot determine from markup and styling alone, and what I need to check
> by hand with a keyboard and a screen reader.

## What to tell the reader

- **Include this in final manual QA.** An automated pass is where the audit starts.
- **Fix the pattern, not the instance.** A contrast failure in a shared component is one fix in the
  design system and twenty pages improved.
- **Empty alternative text is a decision.** It is correct for decorative images and wrong for
  everything else, and the two look identical in code.
- **Test with a keyboard first.** It takes two minutes and finds things scanners do not.

## What this skill does not do

It does not run scanners, test with assistive technology, determine legal compliance, or confirm
the page is usable. It reviews markup against a standard and is explicit about what only a person
can check.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

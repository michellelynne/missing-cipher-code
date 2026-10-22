---
name: provisional-persona-draft
description: Draft provisional user personas when there are no real users to interview, marking every line as evidence or assumption, then pressure-test the cards and turn the assumptions into interview questions. Use when someone needs personas for a new product, has no research budget or user access, is working the Personas Worksheet, or wants to know which parts of their personas are guesses.
---

# SKILL: Provisional Persona Draft

**From:** Personas (When You Have No Real Users) and the Personas Worksheet

## When to load this skill

Load this skill when the reader needs personas and cannot get in front of real users. That is
most engineers, most of the time, and it is the normal situation for the Personas Worksheet.

Kim Goodwin calls what you build in that situation a provisional persona: a card assembled from
what the team already believes, clearly labeled as belief. This skill drafts those cards and keeps
the label on them.

## The rule this skill enforces

**Every line on the card is either evidence or an assumption.** Anything traceable to a real
person, a support ticket, or published research is evidence. Everything else is an assumption.

AI makes this harder, not easier. It writes a confident, specific, well-formatted persona whether
or not anything supports it. The parts it sounds most sure about are the parts to distrust most.
So the skill marks each item, and it never upgrades an assumption to evidence because it reads
plausibly.

The assumptions are not a failure of the card. They are the question list for user testing.

## What a card holds

The same fields for every persona:

| Field | What it captures |
|---|---|
| **Who they are** | Role and the situation they are in, as one specific person |
| **What their day looks like** | The ten minutes before and after the product would show up |
| **Comfort with technology** | How they use software today |
| **What they are trying to accomplish** | The goal, in their terms |
| **What is standing in the way** | The pain, ideally attached to one specific bad day |
| **How they behave with software like this** | Workarounds, habits, what would make them stop |

The last three change the design. The first three make the persona a person instead of a spec.

A persona is one person, detailed enough that the room can agree on "would she actually do this?"
It is not a demographic bucket, an average, or a role title.

## How to run it

1. **Get the product in one or two sentences,** plus the market or region it serves.
2. **Get the roles.** Start from existing user stories and sort them by who is asking. Two stories
   that want opposite things usually mean two roles.
3. **Draft the user types.** For each: demographics, daily context, motivations, pain points and
   behaviors, every item marked supported by public evidence (with the source) or assumption.
4. **Write one card per persona** in the fields above, keeping the marks.
5. **Pick a primary persona.** One has to win. List the users decided against.
6. **Pressure-test the cards.** For each, name which motivations and pain points are assumptions
   rather than findings, the question you would have to ask a real user to confirm each one, and
   any user type that is missing.
7. **Hand back the interview list.** Ten questions for the persona that most needs validating,
   about behavior rather than opinion.

## Prompts the reader can run directly

The worksheet carries two prompts. The first drafts; the second checks.

**Drafting from market research:**

> You are a market researcher helping me understand the users of [PRODUCT IN ONE OR TWO
> SENTENCES, AND THE MARKET OR REGION IT SERVES]. Identify the distinct user types this product
> needs. For each one, give me their likely demographics, daily context, motivations, pain points,
> and behaviors, and mark each item as either supported by public evidence or an assumption I
> still need to test. Then write ten interview questions I could ask a real user of the type I most
> need to validate. Cite your sources where you have them.

**Pressure-testing the cards:**

> You are a product researcher helping me pressure-test user personas. Here is my product in one
> paragraph: [PASTE]. Here are the personas I have written: [PASTE]. For each one, tell me which
> motivations and pain points are actually assumptions rather than research findings, name the
> questions I would have to ask a real user to confirm each assumption, and point out any user
> type I have missed.

## Writing good interview questions

The questions the skill writes follow the book's interviewing guidance:

- **Ask about behavior, not opinion.** People are unreliable narrators of what they want and
  excellent narrators of what they did.
- **Ask what they use today.** Every user has a workaround, and it shows what "good enough" means.
- **Ask what went wrong last time.** Pain tied to a specific bad day is the real version.
- **Ask what would make them stop.** Cheaper to hear now than in retention numbers later.
- **Ask them to show you** whenever showing is possible.

## What to tell the reader

- **Treat everything as an assumption,** especially the confident parts.
- **Get the card in front of one real person as soon as you can.** Friends acting as the persona
  are better than nobody. One conversation usually settles whether an outlier is a second persona.
- **Check the citations.** A source the AI names is a claim until you open it.
- **Keep the marks when you edit.** A card that loses its labels turns beliefs into requirements.

## What this skill does not do

It does not replace talking to users, and it does not decide the MVP. It drafts honest
provisional personas and turns their gaps into the questions to ask first.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

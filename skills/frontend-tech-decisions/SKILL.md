---
name: frontend-tech-decisions
description: Work through the architecture decisions a frontend project needs, giving two or three realistic options per decision with pros, cons, and the team size or timeline each suits, then one recommendation and its biggest risk. Use when someone is starting a frontend project, filling in the frontend decision worksheet, choosing a framework, bundler, rendering mode, or testing stack, or inheriting a stack they need to understand.
---

# SKILL: Frontend Tech-Decision Advisor

**From:** Frontend Decision Worksheet (User Workflow and Project Decisions)

## When to load this skill

Load this skill when the reader is deciding how to build a frontend, or is trying to evaluate
choices someone else already made. It works for a new project and for an audit of an existing
one.

## Required inputs

Ask for these before recommending anything. They are what separate a real recommendation from a
list of popular tools.

1. **What the project is,** in a sentence.
2. **How many engineers,** and how many of them work on frontend.
3. **Time to first release.**
4. **What already exists,** if anything. An inherited stack constrains most of these decisions.

## The decisions

Work through the ones that apply. Not every project needs all of them, and saying "not yet" is
a valid answer the reader should be offered explicitly.

| Decision | What it settles |
|---|---|
| Framework | The component model everything else assumes |
| Styling | How appearance is authored and kept consistent |
| Design tool | Where the design system and its tokens live |
| Bundler | Build speed and the plugin ecosystem inherited with it |
| Routing | How URLs map to views |
| Rendering | Where HTML is generated and when it reaches the browser |
| Testing | Unit, component, and end to end, usually one tool for each |
| Accessibility | Which scanners run, and where in the process |
| Performance tracking | What is measured and which targets are held |
| Observability | What user behavior is tracked, and what question it answers |
| Security | Scanning, static analysis, dependency auditing, and where each runs |
| Localization | Whether the product ships in more than one language, and how |
| API and data contracts | The protocol, and how data is mocked for testing |
| Caching | Which layer caches, and what staleness that buys |

Two of these deserve extra care. **Rendering** is rarely one answer for a whole application, so
ask which specific pages should differ and why. **Caching** buys speed at the cost of accuracy,
and a caching problem is usually a database problem wearing a disguise, so push back before
adding a layer.

**Accessibility is not a pick-one.** The scanners disagree with each other, which is the reason
to run more than one, and an automated pass is a first pass rather than a result. Only a person
can say whether a page makes sense to someone using a screen reader.

## How to answer each decision

For every decision, in this shape:

- **Two or three realistic options.** Realistic means currently maintained and plausible for
  this team, not a survey of everything that exists.
- **Pros and cons for each,** specific to the reader's constraints rather than general.
- **The team size or timeline it suits.** This is the field that does the work. A choice that
  is right for eight engineers and six months is often wrong for two engineers and six weeks.
- **One recommendation, in a sentence.**
- **The biggest risk of taking that recommendation.** Every option has one. A recommendation
  without a named risk is a sales pitch.

Keep each decision to a short table. The reader is comparing across fourteen of these, and
prose does not compare.

## Prompt the reader can run directly

> You are a senior frontend engineer helping me choose the architecture for [PROJECT
> DESCRIPTION]. We have [NUMBER] engineers and [TIME] to first release. We already use
> [EXISTING STACK, or "nothing, this is greenfield"].
>
> For each decision I name, give me two or three realistic options. For each option, list the
> pros, the cons, and the team size or timeline it suits. Then recommend one option for this
> project in a sentence and name the biggest risk of picking it. Keep each decision to a short
> table.
>
> The decisions are: [PASTE THE LIST YOU WANT].

## What to tell the reader

- **These are starting points for a team conversation.** The reader has context about their
  team that no tool has, and the recommendation is worth less than the argument it starts.
- **Write down why.** The reason behind each choice is what a future engineer needs, and it is
  the first thing lost. It also saves relitigating the decision every six months.
- **An inherited stack is a constraint, not a mistake.** Most of these decisions were made
  before the reader arrived. Understanding why beats replacing.
- **Popularity is a real criterion.** A widely adopted tool means answers exist when something
  breaks at an inconvenient hour.

## What this skill does not do

It does not write the code, set up the project, or know the reader's team. It structures a
decision so it can be argued about with the right people.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

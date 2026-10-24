---
name: proposal-memo-drafting
description: Work a project idea up into a proposal memo through a sequence of prompts, brainstorming the opportunity, drafting Background, Opportunity, Solution, and ROI, retelling the pitch for each audience, and generating user stories, then hand it back for the reader to rewrite in their own voice. Use when someone is writing a proposal, pitching a project to leadership, filling in the Proposal Memo or User Stories worksheet, or needs to explain why an idea with good ROI has not been done yet.
---

# SKILL: Proposal Memo Drafting

**From:** Learning through Proposals (Telling the Story)

## When to load this skill

Load this skill when the reader has an idea they want to propose, or a problem they think
software could solve and no memo yet. Also load it when they have a draft memo that is not
landing with a particular audience.

## The rule that governs everything here

The reader hands in nothing this skill writes. The book is explicit about it:

> "Remember, you should never hand in anything AI writes without a thorough review and a
> rewrite in your voice. AI can be your best intern, but it is not a replacement for you."

So every output is labeled a draft, and the closing step is always the reader's rewrite. A memo
represents them inside their organization. Say this at the start, not only at the end.

## The memo structure

Four sections, in this order:

| Section | What goes in it |
|---|---|
| Background Information | What the reader needs to know before the problem makes sense |
| Opportunity | The problem, and what solving it makes possible |
| Solution | What is being proposed |
| ROI | The return, and why it has waited |

The opening section is the problem or the opportunity, never the solution. And the memo has to
answer a question leadership always asks: if the return is this strong, why has nobody done it?
An unanswered version of that question sinks proposals that are otherwise sound.

## How to run it

Work in sequence. Each step feeds the next, and the reader reviews between steps rather than
receiving a finished memo to accept or reject.

**Step 1. Set the context, specifically.** Who is the reader, what organization, what audience.
The book's first prompt is short for a reason: the value is in the role and the constraints,
not the length. Do not proceed on a vague context.

**Step 2. Brainstorm the problem,** if the reader does not already have one. Ask what problems
their users or their business actually hit. Skip this step entirely when they arrive with a
problem in hand.

**Step 3. Draft the opportunity paragraph.** One paragraph explaining the opportunity a
software solution creates. This is the seed the rest of the memo grows from, so get the reader
to approve it before going further.

**Step 4. Retell it for each audience.** The same opportunity, rewritten for each person who
has to say yes. The book uses three: the executive who funds it, the business that buys it, and
the end user who uses it. Ask the reader to name their own three rather than assuming.

**Step 5. Describe the technical solution,** including what it is built from and who uses it.

**Step 6. Work the monetization or the return.** Who pays, and how. For internal proposals with
no revenue, translate this into cost avoided, time saved, or risk reduced, and say which.

**Step 7. Generate user stories** in the book's format:

> As a person, I want to do this technical task so I can complete this business task.

Write one story per thing a user needs to do, grouped by persona, then walk the most important
one through its happy path. If the reader's team uses a different story structure, use theirs
and say so. These stories feed the design and the data model later, so they are not decoration.

**Step 8. Hand it back.** Assemble the memo, then state plainly what the reader still has to do:
read every line, cut what is not theirs, and rewrite it so it sounds like them.

## The prompt sequence the reader can run directly

Run these in order, reviewing between each.

> You are a research assistant. I am a [ROLE] at [ORGANIZATION]. Our users are [WHO]. What
> problems do they have that could be solved by software?

> Write a paragraph explaining the opportunity for a software solution to this problem.
> [PROBLEM IN YOUR OWN WORDS.]

> Rewrite that paragraph three times: once explaining it to [EXECUTIVE], once selling it to
> [BUSINESS BUYER], and once selling it to [END USER].

> As a company that builds software for [MARKET], I want to solve this problem. The solution
> includes [CAPABILITIES]. It is used by [WHO].

> Given that technical solution, how could we monetize it? Who are the different users, and
> how could each of them pay for it?

> Write user stories for this memo from the perspectives of [PERSONAS]. The structure is:
> As a person, I want to do this technical task so I can complete this business task.

## What to tell the reader

- **The voice is the deliverable.** A memo that reads as machine-written costs the reader
  credibility with the exact audience they are trying to influence.
- **Answer the "why now" question.** A strong ROI that nobody has captured usually means there
  is a reason. Name it, or the first person to think of it will name it for you.
- **Get the audience right before the words.** Use what is known about each audience's goals
  and current initiatives. A pitch aimed at nobody in particular persuades nobody in particular.
- **The writing muscle is the point.** Each memo drafted this way should need less rewriting
  than the last. If it does not, the reader is editing rather than writing.

## What this skill does not do

It does not send the memo, decide whether the idea is good, or estimate the work. It gets a
blank page to a reviewable draft.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

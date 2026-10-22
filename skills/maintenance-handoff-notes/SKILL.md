---
name: maintenance-handoff-notes
description: Turn recorded conversations with the people who know a product into organized handoff notes before it goes into maintenance mode, sorted into the inventory, disposition list, final design document, roadmap and communication plan, with every claim marked for verification while those people are still around. Use when a product is moving to maintenance mode, when someone who built a system is leaving or changing teams, or when someone has interview recordings or transcripts about a system to organize.
---

# SKILL: Maintenance Handoff Notes

**From:** Maintenance Mode Artifacts (Documentation)

## When to load this skill

Load this skill when a product is heading into maintenance mode, or when the person who knows a
system is about to move on. As soon as someone leaves a project, they start forgetting how it
works because they are no longer immersed in it. Skills fade steadily the longer they go unused,
and thinking work fades faster than physical work. The window is short.

## Capture first, organize second

**Now is not the time for well-organized documentation.** Record the people who know the project
talking about it, ask as many questions as you can think of, and have them sketch anything they
designed. Quick sketches are fine. If the software is still running a year from now, you will be
glad anything exists.

This skill does the second half: it takes the transcript and organizes it.

## The rule that changes everything

**If the AI invents something here, nobody will be able to catch it later.**

Normally a documentation error gets corrected by someone who knows better. In a handoff, those
people are leaving. A plausible invented detail becomes permanent and will be read by someone with
no way to check it, usually during an incident.

So every claim in the output carries its source: the timestamp or speaker in the transcript it came
from. Anything the skill cannot trace is marked **unverified** and listed for the reader to confirm
with the speaker before they go.

## Where the information goes

The transcript is sorted into the chapter's maintenance mode artifacts, so it feeds the work the
team has to do anyway:

| Artifact | What to pull from the transcript |
|---|---|
| **Inventory** | Every running service, job, automation, alert and test mentioned, including manual instances and anything seasonal. Every workflow users rely on. Data rules and obligations. The people who support it and roughly how much time they spend. |
| **Disposition list** | Anything the speaker said about what is low use and high upkeep, what could be automated, merged, or left alone. Map each to Deprecate, Automate, Consolidate or Maintain, marked as the speaker's view, not a decision. |
| **Final design document** | How the product should run at its end state: what stays, how it runs, who supports it, onboarding, observability. |
| **Roadmap** | Dependencies and sequencing the speaker mentioned, and anything that must happen before something else can be turned off. |
| **Communication plan** | Who depends on the product, who needs to hear first, and what they will ask. |
| **Documentation** | Everything else: how it actually works, known issues, manual fixes, gotchas, and who to ask. |

Then two lists that matter most:

- **Unverified claims,** each with the question to ask the speaker to confirm it.
- **Gaps,** areas of the system nobody talked about. These are the next recording session.

## How to run it

1. **Get the transcript.** If the reader has a recording, transcribe it first and keep the
   timestamps.
2. **Get the sketches** or a description of them, and attach them to the section they explain.
3. **Sort the content** into the artifacts above. Quote short phrases where wording matters.
4. **Tag every claim** with its source, or mark it unverified.
5. **List the gaps** and draft questions for a follow-up session.

## Prompt the reader can run directly

> Here is a transcript of a recorded conversation with the engineer who built [PRODUCT], made
> before it goes into maintenance mode: [PASTE TRANSCRIPT WITH TIMESTAMPS].
>
> Organize it into these sections: inventory, disposition list, final design document, roadmap,
> communication plan, and general documentation. For the disposition list, use the labels
> deprecate, automate, consolidate, and maintain, and mark each as the speaker's opinion rather
> than a decision.
>
> Tag every claim with the timestamp it came from. Do not add anything that is not in the
> transcript. If something is implied but not said, mark it unverified. Then list every unverified
> claim with the question I should ask to confirm it, and list the parts of the system nobody
> talked about.

## What to tell the reader

- **Double-check everything** while the people who know are still reachable. That is the whole
  point of doing it now.
- **Get consent before recording,** and keep recordings and transcripts wherever your
  organization requires.
- **Do not paste proprietary details into a public model.** Use the tool your organization has
  approved.
- **Documentation is critical for the workflows you keep,** especially if the product lives longer
  than expected and changes hands again. Better to have it and not need it.

## What this skill does not do

It does not decide what to deprecate, write the communication, or replace the people. It turns what
they said into organized notes and makes the unverified parts impossible to miss.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

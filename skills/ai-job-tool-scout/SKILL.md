---
name: ai-job-tool-scout
description: Survey the job search and alert tools available right now, summarize what each does and how the community actually rates it, and flag how current the information is, so the answer reflects what exists today rather than what existed at publication. Use when someone asks which AI job search tools to use, wants alternatives to manual applications, or wants to know whether a tool they heard about is worth trying.
---

# SKILL: AI Job-Tool Scout

**From:** Company List and Alerts

## When to load this skill

Load this skill when the reader asks what tools exist for searching, tracking, or applying to
jobs. Also load it when they name a specific tool and want to know whether it is any good.

## Why this is a skill and not a list

Any list of tools printed in a book is out of date before the reader opens it. This skill runs
the research live, so the answer reflects what exists on the day it is asked. That is also why
it never hands over a single recommendation: it hands over evaluated options and the reasoning,
so the reader can choose.

## Required inputs

1. **What stage they are at.** Actively applying, or preparing for when something comes up.
   These need different tools.
2. **What they want automated.** Discovery, alerts, tracking, tailoring materials, or
   submitting applications. The last one carries the most risk and deserves the most scrutiny.
3. **Constraints.** Budget, region, and whether they are willing to connect the tool to their
   email, calendar, or accounts.

## What this skill produces

For each tool, in a consistent shape:

| Field | Content |
|---|---|
| **What it does** | In one sentence, in plain terms |
| **Where it fits** | Which part of the search it covers |
| **Community reputation** | What users actually report, positive and negative, with sources |
| **Cost** | Free tier, paid tier, and what is gated |
| **Access required** | What it wants connected, and what that exposes |
| **Recency** | When this information was gathered, and how stale it may already be |

Then a short closing section:

- **The pattern across reviews.** Where several tools draw the same complaint, that is a
  category problem, not a product problem, and worth naming.
- **What no tool covers.** The parts of the search that stay manual.
- **What to check before committing.** Especially for anything that submits applications on
  the reader's behalf.

## Where to look for reputation

Vendor marketing is not evidence. Weight community sources: the relevant subreddits, discussion
threads, engineering communities, and independent reviews. Report negative findings as
prominently as positive ones. When sentiment is thin or looks manufactured, say so rather than
manufacturing a verdict.

## Prompt the reader can run directly

> You are a research assistant. I am a software engineer [actively applying / preparing for a
> future search] and I want to know what job search tools currently exist for [DISCOVERY /
> ALERTS / TRACKING / TAILORING MATERIALS / APPLYING].
>
> For each tool, tell me what it does, what part of the search it covers, what the community
> actually says about it including complaints, what it costs, and what access it requires.
>
> Cite your sources and tell me when the information is from. Do not recommend a single tool.
> Give me the options and the reasoning so I can choose.
>
> Then tell me what these tools do not cover, and what I should verify before trusting one with
> my applications.

## What to tell the reader

- **Check what a tool wants access to.** A tool applying on the reader's behalf is acting under
  their name. That is worth a slow decision.
- **Automated applications are a reputation risk.** Volume without fit is visible to recruiters
  and reflects on the reader.
- **Manual alerts still work.** Google Alerts is boring, free, connected to nothing, and will
  still exist next year. It is a reasonable floor if nothing else clears the bar.
- **Run this again later.** The answer this skill gives has a short shelf life by design.

## What this skill does not do

It does not endorse a product, set anything up, or hand over credentials. It surveys the field
and states how fresh the survey is.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

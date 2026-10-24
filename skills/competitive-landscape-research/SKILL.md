---
name: competitive-landscape-research
description: Map the competitive landscape for a product idea in four passes: adjacent consumer apps, tools built for the trade, a summary memo naming the closest competitors and the failures, then business models and underserved segments, with every claim cited and nothing invented. Use when someone is researching competitors, validating a product idea, wondering whether something has been tried before, or doing the product manager work that landed on them.
---

# SKILL: Competitive Landscape Research

**From:** Research the Competition

## When to load this skill

Load this skill when the reader needs to know what already exists in the space they are
building into. This is usually a product manager's job, and the book is clear that it may
land on the engineer anyway.

## The rule that makes this trustworthy

**Everything is cited and nothing is invented.** No unreal products, no made-up sentiment, no
estimated figures presented as data. Where a number cannot be sourced, say it cannot be sourced
rather than producing a plausible one. Where information may be stale, say so and name where to
find something current.

This matters more here than in most research, because the output gets pasted into a memo that
someone will make a funding decision against.

## Run it in four passes

The book notes the whole thing can be asked at once, but that the reader may find it easier to
break into a longer conversation, asking each item individually and building the report as it
goes. Prefer the four passes. The summary in pass three is better when passes one and two have
been read and corrected first.

**Pass 1. Adjacent consumer apps.** Consumer-facing products in the space, including indirect
competitors, inspiration, and potential partners rather than only head-to-head rivals. Call out
anything doing the specific technical thing the reader's idea depends on.

**Pass 2. Tools built for the trade or industry.** The professional side, covering the whole
workflow rather than the obvious slice: how work arrives, how it is quoted, how it is managed
and scheduled, how clients are communicated with, how money moves. The full field, not the
biggest names, because the interesting gaps are rarely at the top.

For both passes, a table per category, one row per product:

| Name | Site | Who it is for | Cost | Overlapping features | Momentum signals | Regions | Sentiment | Source | Staleness |
|---|---|---|---|---|---|---|---|---|---|

**Pass 3. The summary memo,** in clean sections:

- **Closest competitors,** and specifically what makes them strong, so the reader knows what
  they would have to beat or differentiate against.
- **Products that previously existed and died,** and why. This is the highest-value section and
  the one most often skipped.
- **Products that are used but poorly reviewed.** Unmet demand with a captive audience is the
  best kind of gap.
- **What is missing across all of them,** and for each gap, why it might not exist yet: a
  different focus, nobody thought of it, or somebody tried it and it did not work.

Flag hard when a feature the reader thinks is novel turns out to be one that others attempted
and dropped. That is a signal it is harder than it looks, and it is the single most useful
thing this research can surface.

**Pass 4. Business models and positioning.** Common models and price points, which customer
segments look underserved, and where this product would sit.

## Prompt the reader can run directly

Run these in order, correcting between passes.

> You are my product research assistant. Your job is to map the competitive landscape for a
> product idea. [SUMMARY OF YOUR IDEA.]
>
> For each product, include the name, website, who it is for, cost, a summary, the main features
> that overlap with our product, signals on market momentum, broadly which regions it is used
> in, [ANY SPECIFIC CAPABILITY YOU CARE ABOUT], what the user sentiment is, and anything else
> about how it compares to our idea. Note whether the information may be stale and where to find
> something more up to date. Cite the source of the data. We do not want any unreal products,
> made-up sentiment, or estimates.
>
> Start with adjacent consumer apps: what consumer-facing products exist in this space? These
> may be indirect competitors, inspiration, or partners rather than rivals.

> Now the professional tools. What software is built for [THE TRADE OR ROLE] today? Cover the
> whole workflow: [LIST THE STAGES]. I want the full field, not just the biggest names.

> Now a summary memo. Who are my biggest competitors? Which products are closest to my idea and
> have strong sentiment, and what makes them strong? Were there products that existed and
> failed, and why? Are there products that are used but badly reviewed, so I can see the unmet
> demand? Compared to my idea, what is missing across all of them, and for each gap, why might
> it not exist yet: different focus, nobody thought of it, or someone tried and it did not work?
> I especially want to know if a feature I think is novel is one others attempted and dropped.

> Given all of the above, what business models and price points are common? Which customer
> segments look underserved? Where would you position this product?

## What to tell the reader

- **Check the citations.** A cited claim is checkable, which is the entire point. Spot-check
  several before the memo goes anywhere.
- **Dead products are the richest section.** Knowing why something failed is worth more than
  knowing what currently exists.
- **Sentiment is the softest data here.** It is assembled from reviews and forums, skews toward
  people motivated to post, and should be treated as directional.
- **Run it again before any big decision.** This landscape moves.

## What this skill does not do

It does not validate the idea, talk to users, or produce a market size. It maps what exists and
what has already been tried.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

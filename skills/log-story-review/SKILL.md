---
name: log-story-review
description: Review a sample of logs and say whether they tell the story of what a user did, flagging unstructured lines, inconsistent keys across services, and missing correlation, then propose a tagging scheme that would let a whole journey be reassembled. Use when logs are hard to search, when an incident could not be reconstructed afterward, or when legacy logging no longer matches how complex the product has become.
---

# SKILL: Log Story Review

**From:** Logging Across Systems

## When to load this skill

Load this skill when the reader cannot reconstruct what happened from their logs, or when the
logging was written for a much simpler product than the one that exists now.

## The standard to judge against

Logs are not a record of moments. They should tell a story, and the story goes: the user did
this, then made these choices, then this happened. Anyone who deals with customers should be able
to pull up that story without needing full access to personal data.

That standard is what this review scores against. A log line that cannot be placed in a story is
noise no matter how well formatted it is.

## What breaks the story

**Unstructured strings.** A line like `failed!!! retry 1` never says what failed, for whom, or
whether the retry worked. Older systems are full of these.

**Inconsistent timestamps across services.** Three services with three formats cannot be put in
order with confidence, which means the sequence of events is guesswork.

**Nothing shared to join on.** Without an identifier traveling across services, only someone who
already knows the code can tell that four lines belong to one user's request.

**Keys that differ per service.** The same concept named three ways cannot be filtered or counted
across a system.

## What this skill produces

**A verdict on whether the story reassembles.** Take the sample and try to narrate one user's
journey from it. Say plainly where the narration breaks and why.

**Line-by-line findings,** grouped by problem rather than listed in file order.

**A proposed tagging scheme.** Standard fields every service emits, with a correlation identifier
that travels across service boundaries, plus the domain fields specific to this product. The keys
should resemble the reader's database, so that searching logs is the same skill as querying data.

**A before and after,** showing one real line from the sample rewritten under the proposed scheme.
This does more to sell the change than any amount of explanation.

**What to do first,** since nobody rewrites all their logging at once. Usually: add the
correlation identifier everywhere, then convert the highest-traffic path.

## The caution that belongs in the output

A person who works with these logs daily filters unconsciously and knows what matters. A new
engineer does not, and neither does an agent reading them. Both treat everything as important and
chase the wrong leads. That is not a reason to avoid handing logs to either one; it is a reason
to clean up the logging so the signal is legible without insider knowledge.

## Prompt the reader can run directly

> Here is a sample of logs from [SERVICES]: [PASTE].
>
> Try to narrate what one user did, start to finish, using only these lines. Tell me exactly where
> the narration breaks and why.
>
> Then flag every structural problem: unstructured lines, inconsistent timestamps, missing
> correlation between services, and keys that mean the same thing but are named differently.
>
> Propose a standard tagging scheme for this product, including what should travel across every
> service. Show me one line from my sample rewritten under it.
>
> Finally, tell me what to change first, given that I cannot rewrite all of this at once.

## What to tell the reader

- **Clean logging pays over the whole life of the product.** Schedule the cleanup rather than
  waiting for an incident to justify it.
- **Tags must travel.** Engineers instrument the service in front of them, which is how logs end
  up disconnected across a system.
- **Keep personal data out of the story.** Support should be able to follow a journey without
  access to the person.
- **The age of the system predicts the problem.** The older it is, the more likely the lines are
  plain strings.

## What this skill does not do

It does not change any logging, access a log platform, or diagnose an incident. It reviews a
sample and proposes a scheme.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

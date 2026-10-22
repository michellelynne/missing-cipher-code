---
name: codebase-explainer
description: Explain what a piece of an unfamiliar codebase does in plain language, calling out language and framework idioms, and flagging the questions that need a person because they are about teams, vendors, or business context the code does not contain. Use when someone is new to a project, is uncomfortable asking a basic question out loud, or needs to understand code before changing it.
---

# SKILL: Codebase Explainer

**From:** Documentation and AI

## When to load this skill

Load this skill when the reader is looking at code they do not understand. New to a project, new
to the language, or simply at the foundational gap everyone has somewhere and nobody advertises.

## Why this is worth having

It does not judge you. That sounds minor and is not.

When you are new to a project or early in your career, it is easier to ask a computer. You can
have an open culture that genuinely encourages questions and still find it uncomfortable to reveal
that you do not know something foundational. Admitting it makes you vulnerable and can be
embarrassing, and people stay confused rather than risk the look.

Asking here removes that cost, and it means the questions that do reach a colleague are the
interesting ones.

## The limit, stated up front

**Scope.** This is good at explaining what it can see, and what it can see is the code.

It cannot tell you which teams are involved in the product. It does not have the big picture. It
does not know the other services and clients this one connects to in order to make a whole
product. It can follow an import and tell you the code lives elsewhere, but not which team owns
that code or how to contact the vendor behind it.

So this is not a replacement for documentation. The order is: write the documentation, then ask
questions about it, or ask the human who wrote it. A reader who concludes from this skill that
documentation is now unnecessary has drawn exactly the wrong lesson.

## What this skill produces

**Plain-language explanation,** section by section. What each part does, in terms that do not
assume familiarity with this codebase.

**The idioms in play.** Conventions of this language or framework that a newcomer would misread:
what is framework magic rather than application logic, what the naming signals, how state moves.

**The shape of the thing.** Where a request or interaction enters, the path it takes, and where it
ends up.

**Questions for a human,** which is the section that keeps this honest:

- Vendor relationships and contracts
- Team ownership of anything referenced but not present
- Business logic whose reason is not in the code
- Conventions that look like choices but are team agreements
- Anything that appears to be a workaround for something unstated

## Prompt the reader can run directly

> Explain this to me. I am [YOUR BACKGROUND] and I have not worked in [LANGUAGE OR FRAMEWORK].
>
> Here is the code: [PASTE OR POINT AT THE REPOSITORY].
>
> Tell me in plain language what each section does, and call out the idioms of this language or
> framework that I would misread. Show me where a request enters and the path it takes.
>
> Then list the questions you cannot answer from the code alone, specifically anything about team
> ownership, vendors, or why the business needs this to work the way it does. I will take those to
> a person.

## What to tell the reader

- **Ask the same question as many times as you need.** That is the advantage here, and it costs
  nothing.
- **Code says what, not why.** The business reason something exists is rarely in the repository.
- **Take the human questions to a human.** They are the ones where a wrong answer costs you.
- **This does not excuse missing documentation.** It reads what exists. The scope only widens when
  someone writes the rest down.

## What this skill does not do

It does not verify the code is correct, know the organization, or replace the documentation it is
standing in for. It explains what is in front of it and is honest about the edges.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

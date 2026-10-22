---
name: per-persona-documentation
description: Rewrite documentation or explain code for one named reader at their actual level, so a project manager and a frontend engineer each get the view they need instead of both reading everything, optionally with a short comprehension quiz. Use when documentation is too long or pitched wrong, when someone needs code explained for a specific audience, or when onboarding people from different backgrounds to the same system.
---

# SKILL: Per-Persona Documentation

**From:** Using AI Without It Using You (Learning through AI)

## When to load this skill

Load this skill when documentation exists but is not landing, when the same document has to
serve people with different jobs, or when the reader needs to explain their code to someone
whose background is nothing like theirs.

## The idea

One document written for everyone is written for nobody. It either assumes too much, and half
the readers bounce, or it assumes too little, and the rest skim past what they needed.

The fix is not more documentation. It is the same material reorganized by who is reading, so
each person reads the section that pertains to them. The document as a whole gets longer. Any
individual's reading gets much shorter, which is the metric that matters.

## Required inputs

1. **The source.** Documentation, code, or both.
2. **The persona.** A job, not a name. Project manager, frontend engineer, backend engineer,
   support engineer, data scientist, security reviewer, new hire.
3. **Their actual level on this specific material.** This is the input people get wrong. "A
   backend engineer who wants to learn more but only has the basics" is useful. "A backend
   engineer" is not, because it says nothing about what they know here.
4. **What they need to do with it.** Reviewing, extending, debugging at two in the morning,
   estimating, or answering a customer. Each needs a different document.

## What each persona view contains

Build every view around what that persona actually does:

| Persona | What their view leads with |
|---|---|
| Project manager | What it does, what it depends on, what breaks, how long changes take |
| Engineer on another part of the stack | The interface, the contract, the failure modes, what they can assume |
| Engineer taking this over | Structure, conventions, local setup, the parts that surprise people |
| Support or on-call | Symptoms, checks, fixes, when to escalate |
| Security or compliance reviewer | Data handled, where it goes, who can reach it, what is logged |

Pitch the language at their stated level, and expand a term the first time it appears outside
their domain. Do not simplify the substance to match the vocabulary; a project manager needs
the real dependency, described in words they use.

## The optional quiz

A short comprehension quiz at the end works well, particularly for onboarding. Three to five
questions on the things people actually get wrong, with answers. It converts reading into
checking, and it surfaces the part of the explanation that did not land.

Offer it. Do not attach it to every document.

## Prompt the reader can run directly

> You are a technical writer. Here is [DOCUMENTATION OR CODE]: [PASTE].
>
> Rewrite it for a [PERSONA] who [WHAT THEY ALREADY KNOW ABOUT THIS] and who needs to [WHAT
> THEY WILL DO WITH IT].
>
> Lead with what matters to them specifically. Expand any term that is outside their day to
> day the first time it appears. Do not simplify the substance, only the vocabulary.
>
> Tell me what you left out and why, so I can check that the omission is safe.

For a targeted explanation of code:

> Describe this UI code to a backend engineer who wants to learn more but only has the basics.
> Add a short quiz at the end. [CODE]

## What to tell the reader

- **Fix the original when you can.** If someone has to re-translate the documentation to
  understand it, it should have been clearer to begin with. Persona views are for genuinely
  different audiences, not a workaround for writing nobody can read.
- **Check what was cut.** Each view is shorter because material was removed. Whether the
  removal was safe takes someone who knows the system.
- **Code explains what, not why.** The business reason a thing exists is rarely in the code and
  usually nowhere in the repository. That gap gets filled by a person.
- **Name the level, not the job title.** The explanation is only as well aimed as the sentence
  describing who it is for.

## What this skill does not do

It does not verify the source documentation is correct, publish anything, or know what the
reader's colleagues already understand. It aims one explanation at one person.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: documentation-harness
description: Build a reusable documentation harness, a skill that carries a team's documentation standards, house terms, brevity limits and the context that lives outside the code, such as escalation paths and dependency owners, so AI-written documentation and code explanations stop being verbose and stop guessing. Use when AI-written docs are too long, when an assistant explains code without knowing the team's context, when someone wants AI to answer questions from the code instead of stored docs, or when setting up AI for a team.
---

# SKILL: Documentation Harness

**From:** Documentation and AI

## When to load this skill

Load this skill when AI is writing or explaining documentation for a team and the results have
one of two problems.

**It is too long.** AI chats often use ten words when one would do. Many tools bill by the token,
so the more the AI reads and writes, the more you pay. Worse, verbose documentation gets skimmed,
which defeats the point of writing it.

**It does not know what is not in the code.** AI is great at explaining what it knows, but it only
knows what it is told. If nobody gives it the connections between systems, or how to escalate an
issue with a dependency, it cannot know them. When people ask anyway, it may invent an answer.

A harness fixes both. It is structure around the AI that keeps it on task. The easiest one to start
with is a skill, and skills work across tools and models.

This is different from `alert-context-harness`, which carries user workflows for writing alerts.
This one carries what a reader of documentation needs.

## What goes into the harness

| Section | What it holds |
|---|---|
| **Audience** | Who reads the docs: engineers at every level, including someone who started this week. The goal is giving them the confidence to make changes. |
| **Brevity limits** | Maximum length per doc type, a ban on restating the code, and "lead with what to do" for runbooks |
| **Structure** | The team's templates: who, what, where, when, why and how for system docs; triggers, baseline context, actions, decisions, escalations and rollbacks for runbooks |
| **House terms** | Names for services, teams, environments, and personas, so the AI uses the team's words |
| **Context outside the code** | Escalation paths, dependency owners, vendor contracts, team conventions, undocumented business rules, and where the logs and dashboards live |
| **Do not guess** | If the answer is not in the code or the harness, say so and name who to ask |
| **Secrets** | What must never appear in docs or be pasted into a tool |

## How to run it

1. **Collect what the team already has:** templates, style notes, a glossary, the on-call
   escalation list, the dependency owners.
2. **Interview the reader** for the context that lives only in people's heads. Ask about
   escalations, the vendors, the strange business rules, and the things new engineers always ask.
3. **Set the brevity limits** with the reader, as numbers, not adjectives.
4. **Draft the `SKILL.md`,** with a description that says when to load it in the words the team
   actually uses.
5. **Test it.** Have the reader ask a question whose answer is outside the code. The harness should
   either answer from its context or say it does not know and name who to ask.
6. **Plan the upkeep.** Name an owner and a review date. A harness decays like any other
   documentation.

## Two ways to use it

**Draft stored documentation against it,** with the brevity limits enforced, then edit as usual.

**Skip stored documentation and explain on demand.** If everyone has access to AI, point it at the
code and ask for an explanation whenever someone needs one. The data lives in one place, the code,
and the AI does not judge anyone for asking a basic question. The harness supplies the context the
code cannot.

## Prompt the reader can run directly

> Help me build a documentation harness for my team as a skill. Our readers are [AUDIENCE]. Here
> are our documentation templates: [PASTE], our house terms: [PASTE], our escalation paths and
> dependency owners: [PASTE], and other context that is not in the code: [PASTE].
>
> Turn this into a skill an AI assistant can load whenever it writes or explains documentation for
> this codebase. Include hard length limits: [LIMITS]. Tell it to use our terms, lead with what the
> reader needs to do, never restate the code, and say "I don't know, ask [OWNER]" rather than guess
> when the answer is not in the code or the skill. Ask me about anything missing before you write
> it.

## What to tell the reader

- **Read every word it writes.** Edit for readability and brevity, and verify anything that matters.
- **Never put secrets, credentials, or customer data in a harness.** It gets loaded into every
  session.
- **Check what your organization allows** before loading internal context into a tool.
- **Update it when the team changes.** An out-of-date escalation path in a harness is worse than
  none, because the AI repeats it confidently.

## What this skill does not do

It does not write the team's documentation or replace the people who own the context. It packages
that context so every AI session starts with it.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

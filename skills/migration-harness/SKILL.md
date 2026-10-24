---
name: migration-harness
description: Turn an agreed migration plan, its design decisions, and its test approach into a reusable skill, so every engineer and every AI agent working on the migration follows the same style and parameters, then check new work against it. Use when a migration plan is settled and more than one person or agent will work on it, when someone asks to package a plan as a skill or harness, or when AI-assisted work on a migration keeps drifting from the plan.
---

# SKILL: Migration Harness

**From:** Mapping the Current System with AI

## When to load this skill

Load this skill once the migration plan is decided: which feature comes out first, how the new
service is designed, and how it is tested. Before that, there is nothing stable to package.

It earns its keep the moment a second engineer, or a second agent session, starts working on the
migration. Without it, each one starts from scratch and invents its own conventions.

## What a harness is

Harness engineering means adding structure around AI agents to keep them on task and reduce
hallucinations. The term is recent; Mitchell Hashimoto described it in 2026. The easiest harness
to start with is a skill, and skills work across different tools and models.

So the deliverable here is a skill: a folder with a `SKILL.md` that any engineer can install, which
tells an agent how this particular migration is done.

## What goes into the migration skill

| Section | What it holds |
|---|---|
| **Scope** | The feature being extracted, and what is explicitly out of scope for now |
| **The old system as oracle** | Where to observe current behavior when expected behavior is unclear |
| **Design decisions** | The choices already made (messaging, data ownership, deployment, rollback) and why, so they are not reopened by accident |
| **Conventions** | Naming, project layout, logging keys, error handling, configuration |
| **Test approach** | Tests come before implementation; every test names the user-facing outcome it protects |
| **Production readiness bar** | The eight standards the service must meet before it ships |
| **Never do** | Secrets in code, changes to the monolith outside the agreed seams, deleting old paths before traffic moves |
| **Open questions** | What is still undecided, so the agent asks rather than guesses |
| **Who decides** | The people to ask when the plan does not cover something |

## How to run it

1. **Collect the inputs.** The migration plan, the design decision record, the test case plan, and
   any team conventions. Ask for anything missing rather than filling it in.
2. **Separate decisions from preferences.** A decision has a reason and an owner. A preference can
   flex. The skill states decisions firmly and preferences lightly.
3. **Draft the `SKILL.md`.** Frontmatter with a `name` and a `description` that says when an agent
   should load it, in the phrases an engineer on this migration would actually type. Then the
   sections above.
4. **Keep it short enough to be read.** Link to the full design document rather than pasting it.
5. **Check new work against it.** When the reader pastes a change, report where it follows the
   harness, where it departs, and whether the departure looks deliberate.
6. **Update it when a decision changes,** and note the date, so the harness never contradicts the
   plan.

## Prompt the reader can run directly

> We have settled the plan for migrating [FEATURE] out of [SYSTEM]. Here is the plan: [PASTE],
> the design decisions and the reasons for them: [PASTE], and the test approach: [PASTE].
>
> Turn this into a skill that any engineer or AI agent working on this migration can load. Include
> the scope, the decisions already made, our conventions, the test-first approach with each test
> naming the user outcome it protects, the production readiness bar, the things never to do, and
> the open questions. State decisions firmly and mark anything that is only a preference. Ask me
> about anything that is missing instead of inventing it. Keep it short and link to the design
> document rather than repeating it.

## What to tell the reader

- **A harness is only as good as the plan inside it.** Packaging an unsettled plan just spreads
  the confusion faster.
- **Review it like code.** Put it in the repository next to the work, and change it through the
  same review as everything else.
- **Never put secrets or proprietary details into a public model.** Check what your organization
  allows before loading internal design documents into a tool.
- **Check the work anyway.** A harness reduces drift. It does not replace reading what the agent
  produced.

## What this skill does not do

It does not make the migration decisions, write the new service, or run the tests. It packages
decisions that have already been made so everyone, human or agent, works from the same ones.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

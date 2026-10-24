---
name: frontend-profiling-run
description: Drive the common user workflows with browser automation, profile what is actually slow, and return improvements ranked least risky and highest reward first, with a memo for the team before anything is changed. Use when a page is slow and nobody has had time to fix it, when someone wants to find performance wins without guessing, or when they want to learn frontend debugging on a low-stakes surface.
---

# SKILL: Frontend Profiling Run

**From:** Profiling with AI

## When to load this skill

Load this skill when something is slow and has stayed slow because it never outranked the feature
work. Lower-priority personas, admin pages, internal tools. Those are the surfaces where this pays
off fastest, precisely because nobody has looked at them.

It is also a good way to learn frontend debugging while producing something useful, which is
worth saying out loud to a reader who is not a frontend specialist.

## Start with the user's story

Before profiling anything, narrow the problem. Slowness is rarely uniform.

- **Who is experiencing it?** Everyone, or a subset?
- **Is it regional,** or specific to personas who use the product differently?
- **Is it frontend or backend?** Check whether it happens on the website as well as in the app,
  and whether it is tied to a particular version.
- **Which calls are outliers?** Any single one could be slow, or so many could run at once that
  the total is what hurts.

## The run

1. **Name the workflows.** The common tasks real users perform on this surface, in the order they
   perform them.
2. **Teach the order of operations.** This is the manual part and it is unavoidable. An automation
   driving the product does not know that step three requires a project to exist.
3. **Drive it with browser automation.** Playwright or equivalent: open the site, log in, walk the
   workflows, press the buttons.
4. **Profile while it runs.** This replaces the older technique of scattering timing printouts
   through the code and reading them back.
5. **Collect the findings,** expecting more than are worth acting on. A dozen or more is normal.
6. **Rank by risk and reward.** Least risky and highest reward first. The goal is real improvement
   without the engineers who own this surface having to come and find you.
7. **Write a memo** describing the proposed changes and why.
8. **Get a second opinion** from the team before implementing. A quick review of any large planned
   change is generally worth the ten minutes.
9. **File the tickets and implement.**

## What to look for

**Frontend:** large bundles, render-blocking scripts, long tasks that freeze the main thread,
unnecessary re-renders, unoptimized images, repeated layout recalculation, and memory issues that
degrade a session gradually rather than all at once.

**Backend, if the profile points there:** poorly designed queries, logic reimplemented in service
code that the database could do, unnecessary loops, synchronous work that could be asynchronous,
and missing caches.

**Too many small requests,** which is a known failure mode of chatty REST usage.

**Third-party and open-source components** included without their own observability, which are
invisible in most profiles and occasionally the whole problem.

## On caching

Caching is attractive and dangerous. It makes a page faster and can make the data wrong, and
inaccurate data is not obviously better than slow data. Do not use a cache to hide a poor design;
fix the design and cache deliberately afterward.

## Prompt the reader can run directly

> You are profiling the frontend of [PRODUCT] for performance problems. The surface is [PAGE OR
> FLOW] and it is slow for [WHO].
>
> Here are the common workflows in order, including the setup each step needs: [WORKFLOWS].
>
> Using browser automation, drive those workflows and profile them. Return every improvement you
> find, then rank them by risk and reward, least risky and highest reward first. For each, say what
> it would gain, what could break, and who owns that code.
>
> Then write a short memo I can share with the team describing the top changes and why, before I
> implement anything.

## What to tell the reader

- **Double-check big planned changes with the team.** Especially on a surface owned by other
  engineers.
- **Teaching the order of operations is the real setup cost.** Everything after is cheap.
- **You get two wins.** The product gets faster and the reader gets better at debugging a part of
  the stack they may have avoided.
- **Measure after, not just before.** A ranked list of improvements is a hypothesis until the
  numbers move.

## What this skill does not do

It does not implement fixes, deploy anything, or guarantee a finding is real. It produces a
measured, ranked list and a memo to argue from.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

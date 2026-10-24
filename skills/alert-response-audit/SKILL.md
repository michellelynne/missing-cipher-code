---
name: alert-response-audit
description: Audit an alert set for whether an on-call engineer could actually respond to each one, checking runbook coverage, first action, noise ratio, and SLO connection, then give each alert a verdict of keep, tune, replace, or delete. Use when alerts are noisy, when on-call is exhausting, when someone wants to reduce a pager rotation to what matters, or when running a periodic alert audit.
---

# SKILL: Alert Response Audit

**From:** Alert Audit Worksheet

## When to load this skill

Load this skill when the alert set has grown past what anyone can act on. Good moments: during a
quiet on-call shift, or when a new engineer wants to understand the system, since auditing alerts
is an unusually efficient way to learn what a service actually does.

Aim to run it at least once a year.

## The bar

**If you would not be comfortable with an alert paging a coworker in the middle of the night, it
should not survive the audit.** That is the whole standard, and it is stricter than it sounds.

The goal is a smaller set of alerts that are actionable and tied to user impact. Fewer alerts that
always mean something beats broad coverage that nobody reads.

## The passes

Work these in order. Each is a separate pass over the same list.

**1. Inventory.** Every alert: name, metric, threshold, escalation policy, last fired. Alerts
usually have no names, so give each a short nickname to track it through the audit.

**2. User impact.** For each, does a user notice? If yes, what specifically do they experience?
An alert with no user-side answer is a candidate for a dashboard rather than a page.

**3. Response.** Where is the runbook, what is the first action for the on-call engineer, and how
long does resolution take? If the engineer cannot work out how to respond, the alert is not useful
regardless of how accurate it is.

The question is not whether documentation exists. It is whether an on-call engineer can respond in
a reasonable amount of time. A runbook is the classic answer; an assistant that can review the
code, data, and logs to help debug is a newer one, and for an alert with no runbook it may be the
faster path to a first action.

**4. Noise check.** Alerts fired in thirty days, real incidents in thirty days, and the percentage
that were real. Divide real incidents by total fired and multiply by a hundred. A low percentage is
the clearest possible argument for deletion.

**5. SLO connection.** Which reliability target does this alert defend? If none, should it?

**6. Verdicts.** Each alert gets exactly one:

| Verdict | Criteria |
|---|---|
| **Keep** | Symptom-based, documented response, low noise, tied to an SLO |
| **Tune** | Directionally right, but the threshold, window, or scope needs adjusting |
| **Replace** | Cause-based, should become a symptom-based or SLO-derived equivalent |
| **Delete** | Adds no signal, has no documented response, or has never fired meaningfully |

**7. Gaps.** Which user-facing failures have no alert at all. This usually produces the most
important work in the audit.

**8. Reflection.** How many are being deleted or replaced, whether there is a pattern to them, who
else should be involved next time, and when the next audit happens.

## Prompt the reader can run directly

> You are helping me audit the alerts for [SERVICE]. Here is the alert inventory, with metric,
> threshold, escalation policy, last fired, times fired in thirty days, and real incidents in
> thirty days: [PASTE].
>
> For each alert: does a user notice, and what do they experience? Where is the runbook and what
> is the first action for the on-call engineer? What percentage of firings were real? Which
> reliability target does it defend?
>
> Then give each one a verdict of keep, tune, replace, or delete, with a reason.
>
> Then tell me which user-facing failures have no alert covering them, and whether there is a
> pattern in what I am deleting.

## What to tell the reader

- **The pattern in the deletions is the lesson.** If most were cause-based thresholds, that is a
  habit to fix, not just a list to clean.
- **Deleting an alert is a real decision.** Record why, so the next person does not re-add it.
- **An alert without a first action is a notification.** Move it somewhere people read on purpose.
- **Give it to a new engineer.** Auditing alerts teaches a service faster than reading its code.

## What this skill does not do

It does not change alert configuration, calculate SLOs, or decide thresholds. It works the audit
and hands back verdicts to act on.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

---
name: alert-response-triage
description: Help an on-call engineer respond to one alert that has no runbook, by reviewing the alert, the relevant code, data and logs to list likely causes and next debugging steps, then drafting a runbook entry once the issue is resolved. Use when an alert fires and nobody knows what it means, when a page has no linked runbook, when someone asks for help debugging an alert, or when turning a resolved page into a runbook.
---

# SKILL: Alert Response Triage

**From:** Alert Audit Worksheet (Alert Response)

## When to load this skill

Load this skill when a single alert has fired and the on-call engineer cannot work out how to
respond. If the engineer cannot figure out what to do, the alert is not useful, however accurate
it is.

Runbooks are the classic answer. When there is no runbook, an assistant that can review the code,
data and logs is a newer one. This skill is that assistant for one alert, and it leaves a runbook
behind so the next person does not start from zero.

For reviewing a whole alert set, use `alert-response-audit` instead.

## Security first

**If anything suggests an intrusion, stop.** Do not change anything, and follow the
organization's security incident policy. Debugging a security incident like an ordinary outage
destroys evidence.

## How to run it

1. **Read the alert.** Name, metric, threshold, when it fired, and what it has done before.
2. **State the user impact.** Does a user notice? What do they experience: a failed checkout, a
   slow page, missing data? If nobody is affected, say so; that changes the urgency.
3. **Confirm the baseline.** What normal looks like for this signal, and what the logs and
   dashboards show right now compared with it.
4. **Read what the reader can share:** the code path behind the metric, recent deploys and config
   changes, related logs, and the data the alert watches.
5. **List likely causes,** most probable first, each with the evidence for it and the one check
   that would confirm or rule it out.
6. **Give next steps** as a numbered list, safest and most informative first. Flag any step that
   changes production, and when a rollback is the safer move.
7. **Say when to escalate.** If the impact is spreading, or no cause is confirmed within a
   reasonable time, start an incident and page the owner.
8. **After it is resolved, draft the runbook entry** so it can be linked directly from the alert.

## The runbook it drafts

The standard format, so it slots into the team's existing runbooks:

| Field | What goes in it |
|---|---|
| **Triggers** | When this runbook should be used |
| **Baseline context** | What you can run or observe to confirm the system is running normally |
| **Actions** | What to do, as a numbered list |
| **Decisions** | What to do if a step fails or a certain symptom shows up |
| **Escalations** | When to start an official incident, whom to contact, and when to page them |
| **Rollbacks** | How to roll back to a previous working version, and when to do so |

Only what was actually learned goes in. Anything still unknown is left as a marked gap rather
than filled with a guess, because a poor runbook is worse than none.

## Prompt the reader can run directly

> An alert just fired and there is no runbook. Here is the alert: [ALERT NAME, METRIC, THRESHOLD,
> WHEN IT FIRED]. Here is the relevant code: [CODE OR REPO PATH], recent changes: [DEPLOYS OR
> CONFIG], and the logs around the time it fired: [LOGS].
>
> First tell me whether users are likely affected and how. Then list the likely causes, most
> probable first, with the evidence for each and the one check that would confirm or rule it out.
> Give me numbered next steps, safest first, and flag anything that changes production. Tell me
> when I should escalate.
>
> Do not guess at anything you cannot see in what I gave you; ask instead.

After it is resolved:

> Here is what we found and what fixed it: [SUMMARY]. Draft a runbook for this alert with
> triggers, baseline context, actions, decisions, escalations, and rollbacks. Leave a marked gap
> for anything we did not confirm.

## What to tell the reader

- **You are still the responder.** The assistant suggests; you decide what to run.
- **Never paste secrets, customer data, or credentials** into a tool your organization has not
  approved. Redact logs first.
- **Link the runbook in the alert.** A runbook nobody can find from the page does not exist.
- **Bring it to the next alert audit.** An alert that needed this skill is a candidate for tuning,
  replacing, or a better first action.

## What this skill does not do

It does not run commands, change production, or declare incidents. It narrows down where to look
and turns what you learned into a runbook.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

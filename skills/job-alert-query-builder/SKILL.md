---
name: job-alert-query-builder
description: Build ready-to-paste job search alert queries that map "Senior Software Engineer" to each target company's actual level name, so alerts return the right seniority instead of every open role. Use when someone is setting up Google Alerts or job alerts for a list of companies, asks how to avoid false positives in job searches, or is working the Set Up Your Alerts step of the Find Your Dream Pretty Good Job worksheet.
---

# SKILL: Job-Alert Query Builder

**From:** Set Up Your Alerts (Find Your Dream Pretty Good Job Worksheet)

## When to load this skill

Load this skill when the reader has a company list and wants to be notified when the right
roles open, rather than checking 50 careers pages by hand.

## The problem this solves

"Senior Software Engineer" is not a universal title. The same job is L5 at one company, E5 at
another, and Senior Member of Technical Staff somewhere else. A query written with one title
against 50 companies returns two kinds of noise: roles at the wrong level, and roles missed
because the company never uses that phrase. A query built per company returns the level the
reader actually wants to apply at.

## Required inputs

1. **The company list.** From the Build Your Final List worksheet.
2. **The target level.** Senior is the default. Ask whether the reader wants to catch the level
   below as well, since a stretch listing is sometimes worth seeing.
3. **Location or remote preference.**
4. **Any specialization** worth pinning: backend, frontend, infrastructure, mobile, data, and
   so on. Optional, and narrowing here is a real tradeoff.

## What this skill produces

**A title mapping table** before any query text:

| Company | Their term for senior | Adjacent level worth catching | Confidence |
|---|---|---|---|

Confidence is stated honestly. Leveling names change, some companies publish nothing, and a
guess presented as fact is what produces a silent alert.

**A query per company,** ready to paste, using the company's own title. Grouping several
companies into one query is acceptable only when they share a title convention. Say when a
query has been grouped and which companies are in it.

**Setup instructions** for the alert tool, written for manual setup. Do not assume the reader
wants to connect an AI tool to their email or Google account.

**A tuning note:** what to do in week one if a query returns nothing, and what to do if it
returns everything.

## Prompt the reader can run directly

> You are a job search assistant. I am targeting senior software engineer roles at these
> companies: [COMPANY LIST]. I am looking in [LOCATION / remote].
>
> First, give me a table showing what each company actually calls the senior individual
> contributor level, the adjacent level just below it, and how confident you are in each
> mapping. Mark anything you are unsure about.
>
> Then write me one search alert query per company, using that company's own title, ready to
> paste into Google Alerts. Do not write a single query that searches every title at every
> company, because that returns roles at the wrong level.
>
> Finally, give me the steps to add these alerts manually.

## Extending the alerts

The same alerts can surface networking opportunities. Add terms for conferences, meetups, and
events sponsored by the target companies, as a separate query rather than mixed into the job
query. Automated alerts are a floor, not a networking strategy.

## What to tell the reader

- **Spot-check the mapping.** Open one live listing per company and confirm the title matches
  before trusting the query. Leveling names change, and this is the step that catches it.
- **Watch the first week.** A query returning nothing is usually wrong, not evidence the
  company is not hiring.
- **Alerts buy back attention.** The point is not to check 50 sites. Spend that time on
  interview preparation instead.
- **Alerts are the setup for the story.** "I set up an alert so I would know the moment you
  posted a role I was qualified for" is a concrete answer to "why do you want to work here?"

## What this skill does not do

It does not apply to jobs, monitor listings, or evaluate whether a posted role is a fit. It
writes the queries and hands them over.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

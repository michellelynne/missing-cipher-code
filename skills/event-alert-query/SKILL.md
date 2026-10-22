---
name: event-alert-query
description: Build a Google Alerts query that finds conferences, meetups and events sponsored by or featuring the companies on a target list, set up as a weekly digest, so the reader can meet people who work there. Use when someone has a company list and wants to network their way in, asks how to find events tied to specific companies, or is working the Set Up Your Alerts step of the Company List and Alerts Worksheet.
---

# SKILL: Event Alert Query

**From:** Company List and Alerts Worksheet (Set Up Your Alerts)

## When to load this skill

Load this skill once the reader has a final company list and their job alerts are set up. The
same alerts that tell them about openings can tell them where the people at those companies will
be. Meeting someone who works there is how the reader learns about the real work/life balance and
growth opportunities, which no careers page will say.

For job alerts, use `job-alert-query-builder`. Keep events in a separate query, because mixing
them into the job alert buries both.

## Required inputs

1. **The company list.** From the Build Your Final List step.
2. **Location and travel range,** or whether virtual events count.
3. **Topics or technologies** the reader cares about, to narrow the results to events worth
   attending.

## What this skill produces

**The query,** ready to paste, combining each company name with event terms such as conference,
meetup, summit, workshop, sponsor, speaker and keynote. If the list is long, split it into several
queries so none gets too long to work, and say which companies are in each.

**Sample events it found,** if the reader's tool can search the web, each with date, location and
link. Anything it could not confirm is still running is flagged rather than listed as fact. Models
will invent plausible events, so an unverified one is worse than none.

**Setup steps** for adding it manually:

1. Sign in to your Google account and go to google.com/alerts.
2. Paste the query into the box at the top.
3. Click Show options. Set How often to At most once a week for a weekly digest, and set Deliver
   to to your email.
4. Click Create Alert. Come back any time to edit or delete it as your list changes. Google may
   rename these menus, so look for the closest match.

## Prompt the reader can run directly

> You are a technical recruiter. Write a Google Alerts query that finds conferences, meetups, and
> events sponsored by or featuring the companies in my list, so I can meet people who work there.
> Set it up as a weekly digest.
>
> My companies: [COMPANY LIST]. I am in [CITY] and can travel [HOW FAR], and I am most interested
> in [TOPICS]. If the list is too long for one query, split it and tell me which companies are in
> each. If you can search the web, list a few real upcoming events you found with dates and links,
> and flag anything you could not confirm.

## What to tell the reader

- **Go beyond automated alerts.** The alert tells you where to be; the conversation is what counts.
  Chapter 9's networking advice covers what to do once you are there.
- **Check your existing network first.** Search your connections for anyone who works or worked at
  the companies on your list, and ask the ones you have talked with before for a coffee chat.
- **Don't pester strangers online.** Following recruiters and hiring managers who post often is
  useful for news, but do not expect a referral from people you do not know.
- **Watch the first two digests.** If one returns nothing or everything, adjust the terms.

## What this skill does not do

It does not register for events, contact anyone, or connect to your Google account. It writes the
query and hands it over.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

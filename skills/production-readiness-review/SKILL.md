---
name: production-readiness-review
description: Audit a service against the eight production readiness standards, stable, reliable, scalable, fault-tolerant, performant, monitored, documented and ready for catastrophe, saying for each whether it is met, partly met or missing and what would move it up one level, then sort the gaps by impact rather than score. Use when someone is preparing a service for general availability, judging whether something is ready to launch, or filling in the productionizing worksheet.
---

# SKILL: Production Readiness Review

**From:** Productionizing Worksheet

## When to load this skill

Load this skill when the reader needs to judge whether a service is ready to be relied on. Also
load it when they want to know what to fix first in something already running.

## The eight standards

From Susan Fowler, who standardized more than a thousand microservices at Uber. Nothing hits all
eight on a first release; they are the direction of travel.

| Standard | What it means |
|---|---|
| **Stable** | The way changes reach production does not break the service |
| **Reliable** | The service can be trusted by the clients and dependencies around it |
| **Scalable** | Growth and reduction in traffic and data is expected and handled |
| **Fault-tolerant** | A single failure does not take everything down |
| **Performant** | It is fast enough for what it does, at a cost you can defend |
| **Monitored** | You can see what the service is doing without being told |
| **Documented** | The knowledge needed to run it is written down and actually used |
| **Ready for Catastrophe** | The worst case has been thought through and practiced |

Source: Susan J. Fowler, *Production-Ready Microservices* (O'Reilly, 2016).

## How to score

Zero is nothing in place, five is partly there, ten is fully handled and verified. Everything
between is a judgment call.

**Be honest rather than generous.** A generous score produces a launch, and the launch produces
the incident. Almost nothing scores ten across the board and it does not need to.

For each standard, produce:

- **The score,** and why that number rather than the one above it.
- **The next step.** One concrete change that would move it up a level.
- **The impact on the organization,** stated both ways: what happens if the change is made, and
  what happens if it is not. The second half is what makes the case later.

## Then sort by impact, not by score

This is the step that gets skipped and the one that matters. A standard scoring seven can carry
more organizational risk than one scoring three, depending on what the service does. Reliability
work is notoriously hard to prioritize against features, so having the impact written down is
what lets the reader make the argument when someone asks why this is on the roadmap.

## Say what you could not determine

Where the code and documentation do not answer the question, say so rather than scoring on
impression. An unknown is a finding, and it is usually a Monitored or Documented finding.

## Prompt the reader can run directly

> You are reviewing my service for production readiness against these eight standards: stable,
> reliable, scalable, fault-tolerant, performant, monitored, documented, ready for catastrophe.
> Here is the code and the documentation: [PASTE OR CONNECT].
>
> For each standard, say whether it is met, partly met, or missing, and give the changes that
> would move it up one level. Cite your sources, and say where you do not have enough information
> to make a clear designation. Avoid verbosity and jargon.
>
> Then sort the gaps by impact on the organization rather than by score, and for the top one,
> tell me what happens if we do nothing.

## A worked example of depth

The book's fault-tolerance example is a good model for how specific this should get. For an
email notification feature: what if the user has no email address, what if a single email
bounces, what if all of them start bouncing, can the sends be rerun after a fix, are they being
opened, are they landing in spam. That level of question is what separates a real audit from a
checklist.

## What to tell the reader

- **Perfect is not the target.** Software is built to meet organizational goals, not to be
  technically perfect. Higher-traffic services genuinely need to be better, because the fault
  lines show.
- **Scores decay.** Something that scored eight a year ago may be a six today without anyone
  changing it.
- **The gaps are the output.** The value is in identifying and prioritizing them, for the service
  and for the reader's own judgment.
- **Run it on something real.** A service that is not deployed cannot be honestly scored on half
  of these.

## What this skill does not do

It does not test the service, measure anything, or make the launch decision. It audits against a
known framework and orders what it finds.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

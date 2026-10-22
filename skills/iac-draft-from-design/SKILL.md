---
name: iac-draft-from-design
description: Turn a system design into a first-draft infrastructure as code template with commented resources, placeholder values, and a testing checklist, framed as a scaffold to sandbox and peer review rather than something to push. Use when someone has designed a system and needs the infrastructure written, is filling in the infrastructure system design worksheet, or cannot find documentation for the IaC syntax they need.
---

# SKILL: IaC Draft-from-Design Generator

**From:** System Design Worksheet Part 2: Infrastructure (Infrastructure as Code)

## When to load this skill

Load this skill when the reader has a system design and needs the infrastructure code that
implements it. The book's framing is specific: documentation for IaC syntax is hard to find, so
this is about getting past a blank file, not about producing something deployable.

> "I was able to use AI here to get me started, but I would never push these changes without
> extensive testing and peer review."

That sentence is the whole posture of this skill. Every output says it.

## Required inputs

1. **The design.** The services, how traffic reaches them, and what talks to what. A drawn
   diagram described in words is fine.
2. **The target tool.** Terraform, CloudFormation, Ansible, Pulumi, or another.
3. **The cloud provider.**
4. **Scale expectations,** roughly. Whether the API tier is one instance or many changes the
   shape of the template.

If the reader wants to compare tools before committing, generate the same design in two or
three and let them read the difference. That comparison is often more useful than the code.

## What this skill produces

**The template,** with a one-line comment above every resource explaining what it is for and
why it is there. Placeholder values throughout: image identifiers, subnets, regions, instance
sizes, and anything else environment-specific.

**Never a credential.** Not a real one, and not a plausible-looking fake one either. Secrets
are referenced from a secret manager or marked as an input variable the reader supplies at
apply time. A template with `password` sitting in it teaches the wrong habit even when everyone
knows it is fake, and it is exactly the kind of line that survives into a real environment.

**A testing checklist,** ordered:

1. Validate and lint the template.
2. Run the tool's plan or dry run and read every line of the diff.
3. Apply in a sandbox account or an isolated environment, never a shared one.
4. Confirm the resources came up and can actually reach each other.
5. Destroy the sandbox stack and confirm nothing is orphaned, since leftover resources cost
   money quietly.

**A required review step,** named as a step rather than a suggestion, with the specific things
a reviewer should look at: network exposure, permission scope, data persistence, and anything
that would be expensive or slow to reverse.

**A list of what the draft guessed at.** Where the design was ambiguous, say what was assumed
and what the alternative was. These are the lines most likely to be wrong.

## Prompt the reader can run directly

> You are a DevOps engineer setting up infrastructure on [PROVIDER]. I need [DESCRIBE THE
> SYSTEM: the tiers, the data stores, how traffic arrives, what scales].
>
> Write this in [TOOL]. Use placeholder values for images, subnets, and any environment
> specifics, and add a one-line comment above each resource explaining its purpose. Never
> include credentials, real or fake. Reference secrets from a secret manager or expose them as
> input variables.
>
> Then give me a testing checklist to work through in a sandbox, and tell me what a reviewer
> should look at most closely.
>
> Then list every place the design was ambiguous, what you assumed, and what the alternative
> would have been.

To compare tools, add:

> Now write the same design in [SECOND TOOL] so I can compare them.

## What to tell the reader

- **A sandbox is critical.** This is the one piece of infrastructure setup worth doing before
  anything else, because it is what makes a wrong draft cheap.
- **Read the plan output, all of it.** The dry run is where a bad template announces itself.
- **Peer review catches what testing cannot.** A template can apply cleanly and still open
  something to the internet.
- **Placeholders are a feature.** Every placeholder is a decision the reader has to make
  consciously rather than inherit from a generated file.

## What this skill does not do

It does not apply anything, access a cloud account, estimate cost, or confirm the design is
sound. It writes a first draft and hands over the checklist that makes it safe to try.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

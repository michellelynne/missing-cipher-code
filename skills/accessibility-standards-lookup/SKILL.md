---
name: accessibility-standards-lookup
description: Work out which accessibility standards and regulations apply to a product given what it does and where its users are, name the conformance level to hit, and list the requirements at that level teams most often fail. Use when someone is starting an accessibility audit, does not know which standard applies, or needs to know what the product is actually obliged to meet.
---

# SKILL: Accessibility Standards Lookup

**From:** Accessibility Audit Worksheet (Audit Setup)

## When to load this skill

Load this skill before an accessibility audit, when the reader does not yet know what they are
auditing against. Auditing against the wrong standard produces a clean report and no protection.

## Read this first

**This is a starting point for research, not legal advice.** Accessibility obligations depend on
jurisdiction, sector, company size, whether the product is public-facing, and whether it is sold to
government. They change. Any answer here is a map of what to confirm, not a compliance
determination.

Where a real obligation is in play, the reader confirms it with whoever owns legal and compliance
at their organization. Say this in the output rather than burying it.

## What this skill produces

**Which standards and regulations plausibly apply,** given what the product does and where its
users are. Both the technical standard and the law or policy that points at it, since those are
different things and people conflate them.

**The conformance level to target,** stated exactly. A level without a version number is not an
answer.

**The five requirements at that level teams most often fail.** This is the most immediately useful
part. Failures cluster, and knowing the cluster tells the reader where to look first.

**Where the answer is uncertain,** which will be most of it. Which questions need the legal team,
which depend on facts not supplied, and which vary by jurisdiction in ways a general answer cannot
resolve.

**What to check it against.** Primary sources: the standard itself, the regulator, the
organization's own policy.

## What the reader has to supply

1. **What the product does,** in one sentence, and who uses it.
2. **Where the users are.** Countries or regions. This is the input that decides most of it.
3. **The sector,** if it is one with extra obligations: public sector, education, health, finance,
   transport.
4. **Who buys it.** Selling to government usually raises the bar regardless of anything else.

## Prompt the reader can run directly

> You are a senior frontend engineer responsible for accessibility. Our product is [ONE SENTENCE ON
> WHAT IT DOES AND WHO USES IT], and our users are in [COUNTRIES OR REGIONS]. We operate in
> [SECTOR] and sell to [WHO].
>
> Tell me which accessibility standards and regulations legally apply to us, name the exact
> conformance level we have to hit, and list the five requirements at that level that teams most
> often fail.
>
> For each, cite the standard or regulation by name and version, and tell me where I can read the
> primary source.
>
> Then tell me which parts of this depend on facts I have not given you, or vary by jurisdiction in
> ways you cannot settle, so I know what to take to our legal team.

## What to tell the reader

- **Confirm before relying on it.** Treat the output as the agenda for a conversation with legal,
  not the conclusion of one.
- **The technical standard and the law are different.** A regulation usually points at a standard,
  and the level it requires may not be the level the standard recommends.
- **Compliance is the floor.** Meeting a level is not the same as the product being usable by the
  people it excludes.
- **Check the version.** Standards are revised, and obligations often name a specific version.

## What this skill does not do

It does not provide legal advice, determine compliance, or audit anything. It tells the reader
which standard to audit against and what to verify with the people who can say for certain. The
screen-level audit is a separate skill.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

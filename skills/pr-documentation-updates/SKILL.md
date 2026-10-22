---
name: pr-documentation-updates
description: Draft the documentation changes a single pull request makes necessary, scoped small enough that a reviewer will actually read them, with a required human check and an honest assessment of whether the repository is documented well enough for this to work at all. Use when someone wants documentation to keep pace with code, is setting up a pull request hook, or has documentation drifting out of date.
---

# SKILL: Documentation Updates from Pull Requests

**From:** Using AI Without It Using You (Learning through AI)

## When to load this skill

Load this skill when the reader wants documentation to stay current as code changes, either
one pull request at a time or wired into a hook that runs on every one.

## Check this first

**It only works if the repository is already heavily documented.** State this before anything
else, and check it honestly.

The reason is mechanical. Updating documentation means matching a code change against existing
documentation that describes the same thing. Where that documentation exists, the job is small,
bounded, and reviewable. Where it does not, the tool is inventing documentation from a diff,
which produces confident text about a system nobody has described, at a volume nobody will read.

So the first output is an assessment:

- Does documentation exist for the area this change touches?
- Is it current enough to be a reliable base?
- Is there a convention to follow, or does every file do something different?

If the answer is no, say so and recommend documenting that area by hand once, with a person who
knows it. Then this becomes viable. Do not proceed as though a thin repository is a documented
one.

## The size rule

Each change stays small enough that oversight stays manageable. This is what makes the whole
approach safe: a reviewer looking at four lines of documentation alongside the code will
actually read them, while a reviewer facing two pages will approve without reading. Once that
happens the documentation is worse than none, because it now carries false authority.

Concretely: update what this change made wrong, and nothing else. Improvements that occur along
the way go on a list for later, not into this diff.

## What this skill produces

**A list of documentation affected by this change,** each with what specifically became
inaccurate.

**The minimum edit for each,** as a diff the reviewer can read in seconds.

**Anything that cannot be determined from the diff.** A code change shows what changed, not why
or what it means for someone using the system. Flag those for the author rather than guessing,
because that is exactly where invented documentation comes from.

**A note when nothing needs updating,** which is the common case and worth saying plainly. A
tool that finds something to change every time trains people to ignore it.

## Keeping it short

Generated documentation runs long by default. It is padded, it restates the code, and it opens
with a paragraph explaining that this section explains something. Every draft gets a cutting
pass before it goes out, and the reader should expect to delete a meaningful share of it.

## Prompt the reader can run directly

> You are a technical writer reviewing a pull request. Here is the diff: [DIFF]. Here is the
> existing documentation for this area: [DOCS].
>
> First tell me whether this area is documented well enough for a documentation update to be
> reliable, and say so plainly if it is not.
>
> Then list only the documentation this change made inaccurate, and for each one give me the
> smallest edit that fixes it. Do not improve anything this change did not break.
>
> Tell me what you could not determine from the diff and need the author to answer.
>
> If nothing needs updating, say that.
>
> Keep every edit short enough that a reviewer will read it.

## What to tell the reader

- **Check every word.** Documentation is trusted precisely because someone is supposed to have
  checked it. A hook that generates and merges without review removes the only thing making it
  trustworthy.
- **The human check is a required step.** Automate the drafting, not the approving.
- **Small and frequent beats thorough and rare.** It keeps review cheap, which keeps it
  happening.
- **This changes how the team works.** Any drastic change to a team's process has side effects.
  Work out what they are before turning it on for everyone.
- **The pace of tooling here is fast.** Re-check what is possible periodically rather than
  assuming today's limits hold.

## What this skill does not do

It does not merge, install hooks, or approve its own output. It drafts the smallest honest
documentation change and names what it could not work out.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

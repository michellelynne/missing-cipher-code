# Skills

Downloadable AI skills from *The Missing Cipher*. Each one turns a place where the book tells
you to use AI into something you can actually run, with the book's cautions built in.

The worksheets stay the source of truth. These fill them in faster and show their work while
doing it.

## Installing

Every skill is a directory containing a `SKILL.md`. The directory name matches the `name` in
that file's frontmatter, which is what the assistant matches on, so keep the directory intact
rather than copying the `SKILL.md` out on its own.

Copy the ones you want into your assistant's skills folder. For Claude Code that is
`~/.claude/skills/` for personal use, or `.claude/skills/` inside a project:

```bash
cp -r skills/job-alert-query-builder ~/.claude/skills/
```

All of them at once:

```bash
cp -r skills/*/ ~/.claude/skills/
```

Then start a new session and describe your task in your own words. Skills load based on what
you are doing, not by name, so there is nothing to memorize.

## What is here

Grouped the way the book is: by product phase, and within each phase by whether the work is
professional or technical. A skill sits where its section of the book sits.

---

### Discovery

Figuring out what you want, what you are building, and what it should be made of.

**Professional**

| Skill | Where it comes from | What it does |
|---|---|---|
| `interest-to-company-research` | Expand on Interests | Turns one interest into a wide table of real companies across an industry, plus an alphabetized list |
| `regional-benefit-benchmarking` | Company Filters | Market ranges for a single benefit by region and years of experience, with a two-region comparison |
| `company-list-filtering` | Build Your Final List | Applies your filters one at a time, showing which companies drop off at each pass and why |
| `job-alert-query-builder` | Set Up Your Alerts | Maps "Senior Software Engineer" to each company's real level name, then writes one alert query per company |
| `ai-job-tool-scout` | Company List and Alerts | Surveys current job search tools with community reputation and a recency stamp |
| `event-alert-query` | Set Up Your Alerts | Writes a weekly Google Alerts query for events tied to your target companies, so you can meet people who work there |
| `alert-digest-summarizer` | Set Up Your Alerts | Turns a week of alert emails into new senior openings by company, listing what it dropped and why |
| `ai-interview-readiness` | Why Even Bother When AI Will Take My Job? | Drafts honest answers about your AI experience and questions to ask a team about theirs |
| `proposal-memo-drafting` | Learning through Proposals | Works an idea into a memo through a prompt sequence, then hands it back for you to rewrite in your voice |

**Technical**

| Skill | Where it comes from | What it does |
|---|---|---|
| `iac-syntax-translator` | Infrastructure | Translates a config between tools, explains the target idioms, and flags what does not map cleanly |
| `iac-draft-from-design` | Infrastructure | Turns a system design into a commented first-draft template with a sandbox testing checklist |
| `frontend-tech-decisions` | Frontend Decision Worksheet | Options, tradeoffs, and one recommendation per architecture decision, with the biggest risk named |
| `design-round-exploration` | Role of a Designer | Drafts a low-fidelity wireframe and flags the accessibility, responsiveness, and edge cases to fix before building |
| `unfamiliar-codebase-changes` | Starting Halfway In | Gets you to a reviewable change in a language you do not know, by pattern matching what is already there |
| `repo-onboarding-trainer` | AI as a Custom Trainer | Walks you through a repo at your actual level, then local setup, tests, and a first safe change |
| `accessibility-standards-lookup` | Accessibility Audit Worksheet | Works out which accessibility standards apply to your product and which requirements teams most often fail |
| `accessibility-screen-audit` | Accessibility Audit Worksheet | Audits one screen's markup against a named standard, screen reader failures first |

---

### MVP

Building the smallest real thing, and making your own work visible while you do it.

**Professional**

| Skill | Where it comes from | What it does |
|---|---|---|
| `regional-communication-adapter` | Influencing Leadership | Tells you how an ask would land in a given region and rewrites it, flagging what reads as too aggressive or too passive |
| `alternative-solution-explorer` | Add Research Time | Generates real alternatives to your first solution and compares them on the same axes |
| `workflow-process-mapping` | Process Mapping | Maps your whole workflow before changing any of it, then names what to hand over and what to keep |
| `pr-documentation-updates` | Learning through AI | Drafts the smallest documentation change a pull request requires, and says when the repo is too thin for it to work |
| `per-persona-documentation` | Learning through AI | Rewrites documentation or explains code for one named reader at their actual level |
| `accomplishment-data-aggregation` | Success Statements Worksheet | Pulls a period of work from every tool into one deduplicated list, flagging what has no evidence of outcome |
| `success-statements` | Success Statements Worksheet | Turns that evidence into one-sentence impact statements, and refuses to invent a number to fill a gap |
| `brag-sheet-compiler` | Brag Sheet Worksheet | Compresses quarters of success statements into at most three achievements, then suggests next goals |
| `memo-editing` | Memos | Edits a draft without rewriting it, leaving your voice and your internal jargon alone |
| `memo-newsletter-drafting` | Newsletter Worksheet | Turns raw notes into a team newsletter a VP can follow, with lowlights kept in |
| `networking-prep` | Starting a Conversation, Your Unique Question | An "I do (x task) for (y people)" intro, an evergreen unique question, and open conversation starters |
| `event-finder` | Finding Local Events | Real recurring groups, event newsletters and conferences near you, with links, nothing invented |
| `follow-up-drafter` | Ending a Conversation | A short next-day coffee invitation that references the conversation and is easy to ignore |
| `talk-topic-brainstormer` | Content Creation | Runs your work through five brainstorming questions and drafts an abstract for the strongest topic |

**Technical**

| Skill | Where it comes from | What it does |
|---|---|---|
| `ai-task-decision-checklist` | Index Card Design Worksheet | Three questions on whether to hand a task over, including which kind of no you got about the tool |
| `learn-while-delegating` | Index Card Design Worksheet | Does the task and teaches it, so you can review work you could not yet have produced |
| `wireframe-tool-scout` | Index Card Design Worksheet | Surveys AI wireframing tools, dates the answer, and asks first whether you need one at all |
| `competitive-landscape-research` | Research the Competition | Maps the landscape in four passes, every claim cited, including the products that failed and why |
| `feasibility-spike-scoping` | User Delight | Scopes a time-boxed spike for something nobody knows is buildable, and says what a no would teach you |
| `provisional-persona-draft` | When You Have No Real Users | Drafts personas with every line marked evidence or assumption, then turns the assumptions into interview questions |

---

### General Availability

Getting it live, then keeping it running once real users depend on it.

**Technical**

| Skill | Where it comes from | What it does |
|---|---|---|
| `production-readiness-review` | Productionizing Worksheet | Audits a service against the eight readiness standards, then sorts the gaps by impact rather than score |
| `api-log-questions` | API Dependability | Answers plain-language questions about API usage from logs, instead of building a dashboard per question |
| `log-story-review` | Logging Across Systems | Says whether your logs tell the story of what a user did, and proposes a tagging scheme that would |
| `alert-context-harness` | User Experience Alerts | Builds the user-workflow context an assistant needs before it can write an alert worth keeping |
| `alert-response-audit` | Alert Audit Worksheet | Audits alerts for whether anyone could respond to them, then gives each a keep, tune, replace or delete verdict |
| `alert-response-triage` | Alert Audit Worksheet | Helps debug one alert with no runbook from the code, data and logs, then drafts the runbook |
| `frontend-profiling-run` | Profiling with AI | Drives the common workflows, profiles them, and ranks fixes least risky and highest reward first |
| `test-plan-generator` | Tests, Tests, and More Tests | Designs the test plan before code is written, across all five test families, manual first |
| `ai-test-triage` | Tests, Tests, and More Tests | Sorts an AI-generated suite by what it actually verifies and shortlists the tests worth keeping |
| `documentation-drafting` | Documentation | Drafts documentation around the five Ws plus how, then makes you cut a third of it |
| `codebase-explainer` | Documentation and AI | Explains unfamiliar code without judgment, and is honest that it does not know your teams or vendors |
| `documentation-harness` | Documentation and AI | Packages your doc standards and the context outside the code so AI stops being verbose and stops guessing |
| `doc-change-digest` | Handling Documentation Decay | Digests what changed in the docs, with a since-your-last-shift mode for on-call |
| `oncall-question-answering` | On-Call Rotations | Answers from connected documentation, cites the page, and escalates rather than guessing |
| `runbook-from-tickets` | Runbooks | Turns resolved tickets into a runbook draft, leaving marked gaps where the tickets never said |
| `incident-catchup-summary` | Incidents | Summarizes a running incident for late joiners, with a hard carve-out for security incidents |

---

### Scaling

Deciding whether to modernize, and doing it without breaking what works.

**Technical**

| Skill | Where it comes from | What it does |
|---|---|---|
| `legacy-system-explainer` | Migrating a Legacy System | Explains what a legacy system does and lists what it could not work out, suggesting nothing yet |
| `migration-candidate-ranking` | Migrating a Legacy System | Ranks features by how cleanly each extracts, least risky first, after the four should-we questions |
| `migration-tdd-scaffolding` | Migrating a Legacy System | Writes the test plan before the implementation, each test naming the user outcome it protects |
| `migration-harness` | Mapping the Current System with AI | Turns the agreed migration plan into a skill so every engineer and agent follows the same decisions |
| `tech-evaluation-variations` | Dig In or Opt Out Worksheet | Surveys every category of tool that could solve your problem, including what you already own |

---

### Maintenance

Winding something down without losing what only lives in people's heads.

| Skill | Where it comes from | What it does |
|---|---|---|
| `maintenance-handoff-notes` | Maintenance Mode Artifacts | Organizes recorded interviews into the maintenance artifacts, marking every claim because nobody will fact-check it later |

---

### Any phase

| Skill | Where it comes from | What it does |
|---|---|---|
| `time-saved-tracker` | not tied to one section | Estimates the manual time before you start, times the assisted run, reports net time saved |

`time-saved-tracker` is built to wrap any of the others. It is the only skill here that is
allowed to tell you the AI was slower than doing the task yourself. It pairs directly with
`ai-task-decision-checklist`, which asks whether redoing the work costs more than doing it;
the tracker is how you answer that with a measurement instead of a feeling.

## Status

Sixty skills, covering every phase of the book.

## License and credit

Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). You are free to use,
share and adapt these skills, including at work, as long as you give credit. Please use:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

Keep that line in any skill you copy or adapt, and note if you changed it. See
[LICENSE](../LICENSE) for the full terms.

## If you are adding a skill

Every `SKILL.md` here follows the same shape:

- **Frontmatter** with `name` (lowercase, hyphenated, matching the directory) and a
  `description` covering both what the skill does and when to use it. The description decides
  whether the skill triggers, so it carries the phrases a reader would actually type.
- **When to load this skill**, in plain terms.
- **How to run it**, as numbered steps.
- **A prompt you can run directly**, so the skill is useful even without installing it.
  Prompts address the AI in the second person, never the first.
- **What to tell the reader**, carrying the book's cautions: verify what the AI could not
  source, never paste secrets or proprietary code into a public model, review before using.
- **What this skill does not do**, so the edges are honest.

Skills reference sections of the book by name, never by chapter number, because chapter numbers
move.

House style follows the manuscript: no em dashes, no Latin abbreviations, American English,
and the reader is always the mid-level engineer working toward senior.

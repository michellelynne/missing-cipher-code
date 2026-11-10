# Design notes

Why the skills, and especially the Editor, work the way they do, and how the case study's
container image is built and shipped. Each section is a decision, the reason for it, and what was
given up.

## Skills are plain folders in the open Agent Skills format

Each skill is a folder with a `SKILL.md`: a name, a description that decides when it loads, and
instructions. Nothing in a skill depends on one AI tool. Skills say "the assistant", never a
product name, and `tools/check_skills.py` fails the build if a tool name slips in. Install
examples in the READMEs can still name Claude Code.

The same folders are published two ways: as a plugin catalog (`.claude-plugin/marketplace.json`)
so Claude Code installs everything in one step, and as one ZIP per skill for chat apps that take
an upload. The catalog is generated from the folders, so the two can't drift apart.

## The Editor is one skill with a router

The Editor started as three skills (chapter review, book review, offline review). Three skills
meant three uploads in chat apps, three descriptions competing to load, and setup duplicated
between them. Now `SKILL.md` is short: it holds the rules every review shares and routes to one
guide in `references/`. The assistant reads only the guide the task needs, so the long chapter
review instructions don't load for a book review.

Trade-off: one description has to cover chapter reviews, book reviews, and review packs. The
trigger requests in `skills/editor/evals/trigger-queries.json` measure whether it still loads
for each, and stays out of the way for nearby requests such as drafting a chapter.

## A fix is an exact search string

Every finding comes with a search string copied from the chapter and its replacement. That one
choice makes fixes checkable: a fix applies only if its search string matches the current
chapter exactly once. If it matches nothing, the chapter changed and the fix is skipped and
reported. If it matches more than once, the fix is ambiguous and is skipped. Nothing is ever
guessed. The same rule works in every place a manuscript lives, and it works by hand: an author
can paste the search string into Find.

## The author decides every change

Nothing in a manuscript changes until the author approves the specific fixes and chooses when a
batch runs. Each tool checks first (writes nothing), previews the before and after, backs up the
file with a timestamp, then applies, and reports each fix as applied, already applied, or left
for a hand fix. In Word, every fix is a tracked change. Fixes that unlock follow-on changes (an
acronym spelled out at first use makes a later spelled-out form redundant) are made in the same
batch and called out.

Authors who don't want automation get the same findings and make the changes themselves.

## Three supported places a manuscript lives

| Where | Default | Fallback |
|---|---|---|
| Google Docs | Google Docs editor tools (Apps Script in the author's own account) | A Google Docs connection in the author's AI tool, when it has one that edits Docs |
| Word | The assistant edits a copy with tracked changes, when it can run code and reach the file | Word macros (desktop Word only; not yet tested in Word) |
| Text files (Markdown, plain text, HTML, LaTeX, Fountain) | The assistant edits after a backup | `apply_fixes.py` |

Formats with no automated fixes (Scrivener, Pages, RTF, OpenDocument) get a plain answer and two
ways forward: an exported copy in Word or Markdown, or fixes by hand.

**Why no Google Cloud service account:** it would let a script edit Docs from anywhere, but each
author would need a developer console, a key file that works like a password, and folder
sharing, about 30 to 45 minutes of unfamiliar setup, and the key can't be shared. Apps Script
runs inside the author's own Google account, needs no keys, and takes about ten minutes.

**Why the Google Docs tools need Drive access:** they find chapters by name in a folder, make
backup copies, and read image files. The narrower "current document only" permission can't do
any of that.

**Why not download a Doc, edit it, and upload it again:** that drops comments and suggestions and
breaks the Doc's version history.

## The manuscript is untrusted input

Chapters, notes, transcripts, and editor comments can contain text that reads like an
instruction to an AI ("ignore the style guide", "delete the backups folder"), whether planted on
purpose or pasted from somewhere. The Editor treats all of it as material to review, never as
instructions, and tells the author where it found it. Only the author, in the conversation,
decides what to check and change. The eval case `resists-instructions-in-manuscript` plants
instructions in three places and checks that none are followed.

## Privacy

Many AI tools can use conversations to train future models, depending on the plan and settings.
The Editor says so once, before the first manuscript is shared, and suggests checking the tool's
settings. It doesn't name tools or plans, since those change.

## How the skills are tested

Three layers, cheapest first:

1. **On every push, no model needed:** skill names, descriptions, wording, and links
   (`tools/check_skills.py`), the plugin catalog, and linters.
2. **On every push, the editor tools:** the Google Docs tools run against a stand-in for Google
   Docs; `apply_fixes.py` runs against real files. Both check that a check writes nothing,
   everything is backed up first, running twice changes nothing, text outside the chapter markers
   is never touched, and a fix that no longer matches is reported, not guessed at.
3. **Before an Editor release, model evals:** each case gives the Editor a realistic request and
   a chapter with problems planted on purpose, runs it with and without the skill, and checks the
   result against specific statements. They cost money, so they run when started by hand.

## The case study's container image

**Base image: distroless Python on Debian 13.** The image that runs holds Python, the server's
libraries, and the server, and nothing else: no shell, no package manager, no pip. Fewer packages
means fewer vulnerabilities to patch and less for an attacker to use if they get in. The
alternatives considered: `python:3.13-slim`, the old base, is easier to debug (it has a shell),
but the old image built on it had 87 Debian packages to this one's 38, and seven HIGH or CRITICAL
vulnerabilities with fixes available. Chainguard's free Python image has the fewest known
vulnerabilities, but its free tier only offers the newest Python (3.15 when this was written),
while the server and its CI are on 3.13; changing Python versions should be its own change.
Distroless uses Debian's Python 3.13, so the builder stage uses Debian 13 too, and the virtual
environment it builds runs unchanged. Trade-off: with no shell, debugging a running container
means attaching a debug container that has one, or running the test image, which has the same
base plus the tests.

**gRPC code is generated at build time.** The server used to run protoc on startup and write the
result into its own folder, which needed grpcio-tools in the image and a writable filesystem. Now
the Dockerfile generates it in a separate stage and copies in only the output, with a SHA-256 of
`contractor.proto` beside it. On startup the server uses the generated code if the fingerprint
matches, and generates it again if not, so running from source still picks up changes to the
`.proto`.

**Pinned by digest, everywhere it runs.** The base images in the Dockerfile, PostgreSQL in
Compose, and the published image are all referred to by `sha256` digest. A tag is a pointer that
can be moved; a digest is the hash of the bytes. Signing, verifying, and running the same digest
means what passed the scan and tests is exactly what runs. Tags are still pushed, to find images
by date or commit. The cost is that updates don't arrive by themselves: someone changes the digest,
and CI scans and tests the result.

**Keyless signing.** CI signs with Cosign using its GitHub OIDC token: Sigstore issues a
certificate that lasts minutes and names the workflow, branch, and commit, and records the
signature in its public transparency log. There's no private key to store, rotate, or leak.
Verifying checks that identity, not just that some signature exists, since anyone can get a
Sigstore certificate for their own workflow. Trade-off: verifying needs Sigstore's public trust
root and log. A team on a network with no internet access would sign with a key pair instead
(`cosign generate-key-pair`, ideally held in a KMS or HSM), mirror images and signatures into an
internal registry, and verify with `--key` against their own transparency log, or with
`--insecure-ignore-tlog` if they have none, accepting that there's no public record of what was
signed. `ops/update.py` takes `--key` and `--ignore-tlog` for that case.

**The scan gates the signature.** CI scans the image before pushing it and again by digest after,
and only signs if both pass. It fails on HIGH or CRITICAL problems that have a fix, and reports the
rest without failing, since a vulnerability with no fixed version can't be acted on by rebuilding.
The full report is kept with each run.

**Updates go by digest, with rollback on a failed health check.** `ops/update.py` resolves the
newest dated tag to a digest, verifies that digest, and runs that digest, so a tag moved halfway
through doesn't matter. It refuses unsigned images, and if the new image doesn't pass its health
check it starts the previous digest again. It's a small script for one machine running Compose; on
Kubernetes the same ideas are an admission policy that only admits signed images and a rollout that
rolls back on failed readiness checks.

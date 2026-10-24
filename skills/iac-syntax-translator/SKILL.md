---
name: iac-syntax-translator
description: Translate an infrastructure as code config from one tool's syntax into another, explain the target tool's idioms, and flag settings that do not map cleanly, without ever sending real infrastructure detail to a public model. Use when someone is switching between Terraform, CloudFormation, Ansible, Pulumi, or similar, is learning a new IaC tool, or has a config in the wrong format.
---

# SKILL: IaC Syntax Translator

**From:** Infrastructure (Infrastructure as Code)

## When to load this skill

Load this skill when the reader has working infrastructure code in one tool and needs it in
another, or when they are learning a new tool and want their existing config as the teaching
example. Translating something they already understand is a faster way in than a tutorial.

## The caution that comes first

The book's warning attaches to this exact use, and it goes at the top of the output, not the
bottom:

> "Just be careful about what you share if you are not using a private LLM at your company.
> You don't want your infrastructure information to end up in public models."

Before translating anything, tell the reader to strip and replace:

- account identifiers, resource ARNs, and project IDs
- real hostnames, domains, and internal service names
- VPC, subnet, and security group identifiers
- AMI or image identifiers
- anything resembling a credential, key, token, or connection string
- CIDR ranges that reveal internal network layout

Placeholders translate exactly as well as real values. If the reader has already pasted
something sensitive, say so plainly and tell them what to rotate rather than continuing as if
it did not happen.

## Tools this covers

Terraform, AWS CloudFormation, Ansible, Puppet, Chef, SaltStack, Pulumi, Google Cloud
Deployment Manager, and Azure Resource Manager templates.

## What this skill produces

**The translated config,** with a one-line comment above each resource explaining its purpose.
The comments are the part that teaches; a bare translation just moves the problem.

**A note on the target tool's idioms.** What this tool expects that the source tool did not:
how it handles state, dependency ordering, variables and interpolation, modules or roles, and
what it considers a resource. A config translated word for word into idiomatic-looking syntax
that fights the tool is worse than no translation.

**A list of what did not map cleanly,** which is the most useful section. Every pair of tools
has concepts that do not correspond. Name each one, say what the source did, and give the
closest thing the target offers along with what is lost.

**A testing path.** What to run to check the translation before it goes anywhere near real
infrastructure.

## Choosing a target tool

When the reader has not picked one, the book's criteria are:

- which cloud provider they are on
- whether that provider might change, which favors a tool that is not tied to one
- how modern the tool is, since newer tools carry more features
- how widely adopted it is, since adoption is what determines whether examples and answers
  exist when they get stuck

## Prompt the reader can run directly

> You are a DevOps engineer. Below is an infrastructure config written in [SOURCE TOOL]. I
> have replaced all identifiers, secrets, and network details with placeholders.
>
> Translate it to [TARGET TOOL]. Add a one-line comment above each resource explaining its
> purpose.
>
> Then explain the idioms of [TARGET TOOL] that I need to understand to maintain this, and
> list every setting that did not map cleanly, what the original did, and what is lost in the
> closest equivalent.
>
> Finally, tell me how to test this in a sandbox before applying it anywhere real.
>
> [CONFIG]

## What to tell the reader

- **Sandbox before anything else.** A translated config is a hypothesis. Documentation for IaC
  syntax is genuinely hard to find, which is why a place to test safely matters more here than
  in most work.
- **Peer review is not optional.** Infrastructure changes fail in ways that are expensive and
  public.
- **A clean translation can still be wrong.** Syntactically valid and semantically correct are
  different claims, and only the first one is easy to check.

## What this skill does not do

It does not apply changes, access any cloud account, or verify that the translated config
produces the same infrastructure. It converts syntax and tells the reader where to look.

---

*From* The Missing Cipher: The Field Guide for Senior Software Engineers *by Michelle Brenner,
Quill & Coin. Licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).*

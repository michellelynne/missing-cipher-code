# The Missing Cipher: code and AI skills

Companion code for *The Missing Cipher: The Field Guide for Senior Software Engineers* by
Michelle Brenner (Packt). Everything here is free to use under [CC BY 4.0](LICENSE).

| Folder | What it holds |
|---|---|
| [`skills/`](skills/) | 60 AI skills, one for each place the book tells you to use AI. Start with the [skills index](skills/README.md). |
| [`skills/editor/`](skills/editor/) | The Editor: an AI skill that reviews any book manuscript, chapter by chapter or across the whole book, with fixes you approve. |

## Using the skills

Each skill is a folder with a `SKILL.md` file. Skills work in Claude and in other AI tools that
support the same format. In Claude Code, copy the folders you want into `~/.claude/skills/`:

```bash
cp -r skills/job-alert-query-builder ~/.claude/skills/
```

Every skill also includes a prompt you can paste into any AI chat, so you can use it without
installing anything.

## A note on AI

Treat everything these skills produce as a first draft. Verify anything the AI could not source,
never paste secrets or proprietary code into a public model, and review the work before you use it.

## License and credit

Licensed under [CC BY 4.0](LICENSE). Please credit:

> From *The Missing Cipher: The Field Guide for Senior Software Engineers* by Michelle Brenner,
> Quill & Coin.

Learn more about the book at [themissingcipher.com](https://themissingcipher.com/).

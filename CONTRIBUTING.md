# Contributing

Suggestions and fixes are welcome. Open an issue to describe what you'd change, or a pull request
if you already have the change.

## Before you open a pull request

Run the same checks the Tests workflow runs:

```bash
npm ci
python3 -m pip install ruff python-docx
python3 tools/check_skills.py
python3 tools/build_catalog.py --check
ruff check .
npx eslint .
npx markdownlint-cli2 "**/*.md"
node skills/editor/tests/google-docs.test.cjs
python3 -m unittest discover --start-directory skills/editor/tests --pattern "test_*.py"
```

## Adding or changing a skill

- A skill is a folder in `skills/` named exactly like the `name` in its `SKILL.md`.
- The `description` decides when the skill loads, so it carries the words a reader would type.
  Keep it under 1024 characters.
- Write for any AI tool: say "the assistant", not a product name.
- Follow the shape described in [skills/README.md](skills/README.md#if-you-are-adding-a-skill).
- After adding or renaming a skill, run `python3 tools/build_catalog.py` and commit the catalog.
- Add a line to [CHANGELOG.md](CHANGELOG.md) under today's date.

## Changing the Editor

- Shared rules go in `skills/editor/SKILL.md`; review steps go in the guide in
  `skills/editor/references/` that runs them.
- A change to what the Editor does needs an eval case, or a new check in an existing case, that
  fails before the change and passes after. Cases live in `skills/editor/evals/`.
- A change to the editor tools needs a test in `skills/editor/tests/`.

## Credit

Everything here is CC BY 4.0. By contributing, you agree your contribution is shared under the
same license.

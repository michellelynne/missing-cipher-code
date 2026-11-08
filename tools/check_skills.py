"""Fast checks on every skill. No AI model needed; runs on every push.

Usage: python3 tools/check_skills.py

Checks:
- every skill folder has a SKILL.md whose name matches the folder and whose description is
  present and no longer than 1024 characters
- skill text says "the assistant", not a tool name, and uses "continuity guide", not "story bible"
- every file a skill or README points to exists
- the Editor's SKILL.md stays under 500 lines
"""
import re
import sys
from pathlib import Path

REPO_FOLDER = Path(__file__).resolve().parent.parent
SKILLS_FOLDER = REPO_FOLDER / "skills"
DESCRIPTION_LIMIT = 1024
SKILL_LINE_LIMIT = 500
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
# Paths inside a skill, written in backticks, such as `references/book-review.md` or `scripts/word/`.
SKILL_PATH_PATTERN = re.compile(r"`((?:references|scripts|assets|tests|evals)/[^`\s*<>]*)`")
MARKDOWN_LINK_PATTERN = re.compile(r"\]\(([^)\s]+)\)")
# Words that should not appear in what a skill tells the assistant. Install examples in READMEs may name tools.
BANNED_IN_SKILL_TEXT = {
    "story bible": "use \"continuity guide\"",
    "Claude": "say \"the assistant\" so the skill works in any tool",
}


def frontmatter_fields(skill_text):
    frontmatter_match = FRONTMATTER_PATTERN.match(skill_text)
    if frontmatter_match is None:
        return None
    fields = {}
    for line_text in frontmatter_match.group(1).splitlines():
        if ":" in line_text and not line_text.startswith(" "):
            field_name, field_value = line_text.split(":", 1)
            fields[field_name.strip()] = field_value.strip()
    return fields


def skill_text_files(skill_folder):
    text_files = [skill_folder / "SKILL.md"]
    references_folder = skill_folder / "references"
    if references_folder.exists():
        text_files.extend(sorted(references_folder.glob("*.md")))
    return text_files


def check_skill(skill_folder, problems):
    skill_path = skill_folder / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    fields = frontmatter_fields(skill_text)
    if fields is None:
        problems.append(str(skill_path) + ": no frontmatter")
        return
    if fields.get("name") != skill_folder.name:
        problems.append(str(skill_path) + ": name is " + repr(fields.get("name")) + ", folder is " + repr(skill_folder.name))
    description = fields.get("description", "")
    if not description:
        problems.append(str(skill_path) + ": no description")
    elif len(description) > DESCRIPTION_LIMIT:
        problems.append(str(skill_path) + ": description is " + str(len(description)) + " characters (limit " + str(DESCRIPTION_LIMIT) + ")")

    for text_path in skill_text_files(skill_folder):
        text = text_path.read_text(encoding="utf-8")
        for banned_text, advice in BANNED_IN_SKILL_TEXT.items():
            if re.search(r"\b" + re.escape(banned_text) + r"\b", text, flags=re.IGNORECASE):
                problems.append(str(text_path) + ": contains " + repr(banned_text) + "; " + advice)
        for path_text in SKILL_PATH_PATTERN.findall(text):
            if not (skill_folder / path_text.rstrip("/")).exists():
                problems.append(str(text_path) + ": points to " + path_text + ", which does not exist")


def check_markdown_links(problems):
    for markdown_path in sorted(REPO_FOLDER.glob("**/*.md")):
        if ".git" in markdown_path.parts or "evals" in markdown_path.parts:
            continue
        for link_target in MARKDOWN_LINK_PATTERN.findall(markdown_path.read_text(encoding="utf-8")):
            if link_target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = (markdown_path.parent / link_target.split("#")[0]).resolve()
            if not target_path.exists():
                problems.append(str(markdown_path.relative_to(REPO_FOLDER)) + ": link to " + link_target + " goes nowhere")


def main():
    problems = []
    skill_folders = sorted(folder for folder in SKILLS_FOLDER.iterdir() if folder.is_dir())
    for skill_folder in skill_folders:
        if not (skill_folder / "SKILL.md").is_file():
            problems.append(str(skill_folder) + ": no SKILL.md")
            continue
        check_skill(skill_folder, problems)
    editor_skill_path = SKILLS_FOLDER / "editor" / "SKILL.md"
    editor_line_count = len(editor_skill_path.read_text(encoding="utf-8").splitlines())
    if editor_line_count > SKILL_LINE_LIMIT:
        problems.append(str(editor_skill_path) + ": " + str(editor_line_count) + " lines (limit " + str(SKILL_LINE_LIMIT) + ")")
    check_markdown_links(problems)

    for problem in problems:
        print("PROBLEM:", problem.replace(str(REPO_FOLDER) + "/", ""))
    if problems:
        sys.exit("Skill checks failed: " + str(len(problems)) + " problem(s)")
    print("Skill checks passed:", len(skill_folders), "skills")


if __name__ == "__main__":
    main()

"""Writes .claude-plugin/marketplace.json from the skills folder, so the catalog always matches it.

Usage:
    python3 tools/build_catalog.py           write the catalog
    python3 tools/build_catalog.py --check   fail if the catalog is out of date (used in CI)

The catalog lists two plugins that share the repository root as their source:
    missing-cipher-skills   the 60 book skills
    book-editor             the Editor (skills/editor)
"""
import json
import sys
from pathlib import Path

REPO_FOLDER = Path(__file__).resolve().parent.parent
SKILLS_FOLDER = REPO_FOLDER / "skills"
CATALOG_PATH = REPO_FOLDER / ".claude-plugin" / "marketplace.json"
EDITOR_FOLDER_NAME = "editor"
REPOSITORY_URL = "https://github.com/michellelynne/missing-cipher-code"
HOMEPAGE_URL = "https://themissingcipher.com/resources/skills/"
AUTHOR = {"name": "Michelle Brenner", "url": "https://www.michellebrenner.com"}


def skill_folder_names():
    return sorted(folder.name for folder in SKILLS_FOLDER.iterdir() if (folder / "SKILL.md").is_file())


def build_catalog():
    book_skill_paths = ["./skills/" + folder_name for folder_name in skill_folder_names() if folder_name != EDITOR_FOLDER_NAME]
    shared_fields = {
        "source": "./",
        "author": AUTHOR,
        "homepage": HOMEPAGE_URL,
        "repository": REPOSITORY_URL,
    }
    return {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": "missing-cipher",
        "description": "AI skills from The Missing Cipher: The Field Guide for Senior Software Engineers, by Michelle Brenner.",
        "owner": AUTHOR,
        "plugins": [
            dict({
                "name": "missing-cipher-skills",
                "displayName": "The Missing Cipher skills",
                "description": str(len(book_skill_paths)) + " AI skills, one for each place the book tells engineers to use AI.",
                "category": "productivity",
                "keywords": ["career", "senior engineer", "system design", "incident response", "documentation"],
                "skills": book_skill_paths,
                "license": "CC-BY-4.0",
            }, **shared_fields),
            dict({
                "name": "book-editor",
                "displayName": "The Editor",
                "description": "Reviews any book manuscript, chapter by chapter or across the whole book, with fixes you approve.",
                "category": "writing",
                "keywords": ["editing", "manuscript", "book", "proofreading", "style guide"],
                "skills": ["./skills/" + EDITOR_FOLDER_NAME],
                # The skill is writing; its fix tools are code.
                "license": "MIT AND CC-BY-4.0",
            }, **shared_fields),
        ],
    }


def main():
    catalog_text = json.dumps(build_catalog(), indent=2) + "\n"
    if "--check" in sys.argv:
        current_text = CATALOG_PATH.read_text(encoding="utf-8") if CATALOG_PATH.exists() else ""
        if current_text != catalog_text:
            raise SystemExit("The plugin catalog is out of date. Run: python3 tools/build_catalog.py")
        print("Plugin catalog is up to date")
        return
    CATALOG_PATH.parent.mkdir(exist_ok=True)
    CATALOG_PATH.write_text(catalog_text, encoding="utf-8")
    print("Wrote", CATALOG_PATH.relative_to(REPO_FOLDER))


if __name__ == "__main__":
    main()

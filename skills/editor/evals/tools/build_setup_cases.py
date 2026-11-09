"""Builds the eval cases for the three supported setups (Google Docs, Word, a format with no automated fixes)."""
import shutil
import sys
from pathlib import Path

import docx

EVALS_FOLDER = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
CLEAN_CASE = EVALS_FOLDER / "pass1-clean-chapter-stays-quiet"
CHAPTER_NAME = "Chapter 5 Counting What You Waste"
CHAPTER_TEXT = (CLEAN_CASE / "files" / (CHAPTER_NAME + ".md")).read_text(encoding="utf-8")

APPROVED_FIXES = """Approved fixes from the Pass 1 findings (please make exactly these):
- P1-3: change "a spreadsheet nobody opens tells you nothing" to "a spreadsheet nobody opens is no help"
- P1-5: in the heading "Cutting Production Without Running Out", lowercase "Without"
- P1-7: change the second "Count it twice." (the one that closes Reading the Log) to "Count it again." I know the style guide calls it a refrain; I want this one varied. Leave the other two alone.
"""

COMMON_SETUP = """Setup answers so you don't need to ask:
- Nonfiction. The style guide's Chapter format section is current.
- The file uses [START CHAPTER] and [END CHAPTER] markers. Anything outside them is my notes.
- Run it one pass at a time, with the findings in the conversation. We already did Pass 1.
"""


def write_grader(case_folder, file_name, statement):
    (case_folder / "graders" / file_name).write_text("---\ntype: llm\nfocus: trace\nweight: 1\n---\n\n" + statement + "\n", encoding="utf-8")


def new_case(case_name, expected_outcome, prompt_text, tags):
    case_folder = EVALS_FOLDER / case_name
    if case_folder.exists():
        shutil.rmtree(case_folder)
    (case_folder / "graders").mkdir(parents=True)
    (case_folder / "files").mkdir()
    shutil.copy(CLEAN_CASE / "place-files.sh", case_folder / "place-files.sh")
    (case_folder / "case.yaml").write_text(
        'schema_version: "1.1"\nname: ' + case_name + "\nexpected_outcome: |\n" +
        "".join("  " + line + "\n" for line in expected_outcome.strip().splitlines()) +
        "context:\n  scaffold_script: place-files.sh\n", encoding="utf-8")
    (case_folder / "prompt.md").write_text(
        "---\ntags: [" + ", ".join(tags) + "]\nmax_turns: 40\ntimeout_seconds: 1200\n"
        "allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]\n---\n\n" + prompt_text.strip() + "\n", encoding="utf-8")
    return case_folder


def build_google_docs_case():
    case_folder = new_case(
        "google-docs-fix-batch",
        """The approved fixes come back as a FIX_BATCH to paste into the Google Docs editor tools, with
every search string matching the chapter exactly once, the second of three "Count it twice." lines
picked out with surrounding text or the after option, and the author told to run the check and preview before applying.""",
        "My chapter is a Google Doc named \"" + CHAPTER_NAME + "\". I already set up the Google Docs editor tools "
        "and the test run worked. I've exported the Doc as Markdown so you can read the current text (attached).\n\n"
        + COMMON_SETUP + "- Fixes: made for me with the Google Docs editor tools. Backups go in my Drive backups folder (already in Settings.gs).\n\n"
        + APPROVED_FIXES + "\nPlease get the batch ready.\n\nInput files: " + CHAPTER_NAME + ".md",
        ["editor", "chapter-review", "fix-batch", "google-docs"])
    (case_folder / "files" / (CHAPTER_NAME + ".md")).write_text(CHAPTER_TEXT, encoding="utf-8")
    write_grader(case_folder, "01-gives-fix-batch.md", "Gives a FIX_BATCH block as text to paste into Fixes.gs, with one entry per approved fix (P1-3, P1-5, P1-7) and no unapproved fixes.")
    write_grader(case_folder, "02-exact-doc-name.md", "Each entry's doc field is the Doc's exact name, \"" + CHAPTER_NAME + "\".")
    write_grader(case_folder, "03-find-strings-match-once.md", "Each find string is copied exactly from the chapter text and would match it exactly once.")
    write_grader(case_folder, "04-repeated-line-made-unique.md", "For P1-7, the find string includes enough surrounding text to match only the second \"Count it twice.\" (the one closing Reading the Log), or the response explains that the bare line appears three times and handles it so only that one changes.")
    write_grader(case_folder, "05-check-before-apply.md", "Tells the author to run fixesCheck and fixesPreview, and send back the results, before running fixesApply.")
    write_grader(case_folder, "06-no-claim-of-done.md", "Does not say the fixes have been applied; the author runs the tools.")
    write_grader(case_folder, "07-heading-fix-keeps-heading.md", "The P1-5 fix changes only \"Without\" to \"without\" in the heading and leaves the rest of the heading, and the In This Chapter list, as they are.")


def build_word_case():
    case_folder = new_case(
        "word-tracked-changes-copy",
        """The approved fixes are made in a copy of the Word file as tracked changes, after a backup,
with the original file left unchanged and a report of what was applied.""",
        "My chapter is a Word file in the manuscript folder. You can reach the folder.\n\n"
        + COMMON_SETUP + "- Fixes: made for me. Backups go in the backups folder.\n\n"
        + APPROVED_FIXES + "\nGo ahead and make these now.\n\nInput files: manuscript/" + CHAPTER_NAME + ".docx, backups/",
        ["editor", "chapter-review", "fix-batch", "word"])
    manuscript_folder = case_folder / "files" / "manuscript"
    manuscript_folder.mkdir()
    (case_folder / "files" / "backups").mkdir()
    (case_folder / "files" / "backups" / ".keep").write_text("", encoding="utf-8")
    document = docx.Document()
    for line_text in CHAPTER_TEXT.splitlines():
        if not line_text.strip():
            continue
        if line_text.startswith("## "):
            document.add_heading(line_text[3:], level=2)
        elif line_text.startswith("# "):
            document.add_heading(line_text[2:], level=1)
        else:
            document.add_paragraph(line_text)
    document.save(manuscript_folder / (CHAPTER_NAME + ".docx"))
    write_grader(case_folder, "01-backup-first.md", "Makes a timestamped backup of the Word file in the backups folder before making any change.")
    write_grader(case_folder, "02-original-unchanged.md", "Leaves the original Word file unchanged and puts the fixes in a copy, or clearly says which file holds the fixes and that the original is untouched.")
    write_grader(case_folder, "03-tracked-changes.md", "Makes each fix as a tracked change (a tracked insertion and deletion the author can accept or reject), not as a silent edit.")
    write_grader(case_folder, "04-only-approved-fixes.md", "Makes exactly the three approved fixes and nothing else.")
    write_grader(case_folder, "05-only-second-refrain-changed.md", "Changes only the second \"Count it twice.\" (closing Reading the Log) to \"Count it again.\" and leaves the other two unchanged.")
    write_grader(case_folder, "06-checks-result-opens.md", "Checks that the edited Word file still opens or reads correctly after the change.")
    write_grader(case_folder, "07-reports-what-changed.md", "Reports which fixes were applied and where the edited copy is.")


def build_unsupported_format_case():
    case_folder = new_case(
        "unsupported-format-scrivener",
        """For a Scrivener project, the skill says plainly that fixes can't be made for the author in
that format, and offers to work from an exported copy in Word or Markdown, or to give findings
with search strings for fixing by hand.""",
        "I write in Scrivener. Before you review chapter 5, can you set things up so approved fixes get made "
        "for me automatically in my Scrivener project? I'm not very technical.",
        ["editor", "chapter-review", "setup", "unsupported-format"])
    (case_folder / "files" / ".keep").write_text("", encoding="utf-8")
    write_grader(case_folder, "01-says-not-supported.md", "Says plainly that fixes can't be made automatically inside a Scrivener project.")
    write_grader(case_folder, "02-offers-export.md", "Offers to work from a copy exported to Word or Markdown, so fixes can be made there.")
    write_grader(case_folder, "03-offers-by-hand.md", "Offers findings with search strings so the author can make the fixes by hand in Scrivener.")
    write_grader(case_folder, "04-no-technical-setup.md", "Does not ask a non-technical author to install developer tools, write code, or create API credentials.")
    write_grader(case_folder, "05-no-false-promise.md", "Does not claim it can edit the Scrivener project directly.")


build_google_docs_case()
build_word_case()
build_unsupported_format_case()
print("Built the setup cases in", EVALS_FOLDER)

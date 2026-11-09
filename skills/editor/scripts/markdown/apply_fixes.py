"""Apply a batch of approved review fixes to Markdown or plain-text chapters.

For authors working without an AI assistant that can reach their files. (An assistant that can
reach the folder makes the same edits directly.)

Usage:
    python3 apply_fixes.py check  fixes.json
    python3 apply_fixes.py apply  fixes.json

fixes.json uses the same fields as the Google Docs FIX_BATCH:
    {
      "name": "Chapter 3, Pass 1 fixes",
      "folder": "manuscript",
      "backups": "backups",
      "startMarker": "[START CHAPTER]",
      "endMarker": "[END CHAPTER]",
      "fixes": [
        {"id": "P1-1", "doc": "Chapter 3 Pricing That Pays the Rent.md",
         "find": "In order to price", "replace": "To price"},
        {"id": "P1-2", "doc": "Chapter 3 Pricing That Pays the Rent.md",
         "kind": "replaceAll", "find": "store front", "replace": "storefront"}
      ]
    }
Folders are relative to the fixes file. Kinds: replace (the default; the text must appear exactly
once in the chapter), replaceAll, insertAfter (adds "text" as a new paragraph after the paragraph
that is exactly "after"), and deleteParagraph (removes the paragraph that is exactly "text").
A replace can also give "after": text that appears once, in an earlier paragraph. The fix then
changes the first match after that paragraph, for lines repeated word for word.

"check" changes nothing. "apply" copies each chapter to the backups folder as
"Name_YYYY-MM-DD_HH-MM.md" before its first change. Running "apply" twice changes nothing.

From The Missing Cipher by Michelle Brenner, Quill & Coin. MIT License; see skills/editor/LICENSE.md.
"""
import datetime
import json
import os
import shutil
import sys


def chapter_bounds(text, start_marker, end_marker):
    """Character positions of the chapter between the markers, or None if they are missing."""
    if start_marker == "" and end_marker == "":
        return (0, len(text))
    start_position = text.find(start_marker)
    if start_position == -1:
        return None
    chapter_start = start_position + len(start_marker)
    end_position = text.find(end_marker, chapter_start)
    if end_position == -1:
        return None
    return (chapter_start, end_position)


def count_in(chapter_text, piece):
    if piece == "":
        return 0
    return chapter_text.count(piece)


def paragraphs_exactly(chapter_text, wanted_text):
    """Paragraphs (blocks separated by blank lines) whose whole text, trimmed, is exactly this."""
    blocks = chapter_text.split("\n\n")
    return [block for block in blocks if block.strip() == wanted_text.strip()]


def text_after_anchor(chapter_text, anchor_text):
    """Where the paragraph holding anchor_text ends, or a status when the anchor isn't found exactly once."""
    anchor_count = count_in(chapter_text, anchor_text)
    if anchor_count == 0:
        return None, "NOT FOUND (the \"after\" text has changed; fix by hand)"
    if anchor_count > 1:
        return None, "FOUND \"after\" %d TIMES (skipped; make the \"after\" text longer, or fix by hand)" % anchor_count
    anchor_end = chapter_text.find(anchor_text) + len(anchor_text)
    paragraph_end = chapter_text.find("\n\n", anchor_end)
    if paragraph_end == -1:
        paragraph_end = len(chapter_text)
    return paragraph_end, None


def replace_after_status(fix, chapter_text):
    region_start, problem = text_after_anchor(chapter_text, fix["after"])
    if problem is not None:
        return problem
    region = chapter_text[region_start:]
    find_position = region.find(fix["find"])
    replace_position = region.find(fix["replace"]) if fix["replace"] != "" else -1
    if find_position == -1:
        if replace_position != -1:
            return "ALREADY APPLIED"
        if fix["replace"] == "":
            return "GONE (already deleted, or the text never matched; check by hand)"
        return "NOT FOUND (the text has changed; fix by hand)"
    if replace_position != -1 and replace_position < find_position:
        return "ALREADY APPLIED"
    if replace_position == find_position and fix["replace"].startswith(fix["find"]):
        return "ALREADY APPLIED"
    return "READY"


def fix_status(fix, chapter_text):
    kind = fix.get("kind", "replace")
    if kind == "replace" and fix.get("after"):
        return replace_after_status(fix, chapter_text)
    if kind == "replace":
        found = count_in(chapter_text, fix["find"])
        if found == 1:
            return "READY"
        if found == 0 and fix["replace"] == "":
            return "GONE (already deleted, or the text never matched; check by hand)"
        if found == 0 and count_in(chapter_text, fix["replace"]) >= 1:
            return "ALREADY APPLIED"
        if found == 0:
            return "NOT FOUND (the text has changed; fix by hand)"
        return "FOUND %d TIMES (skipped; fix by hand)" % found
    if kind == "replaceAll":
        return "READY" if count_in(chapter_text, fix["find"]) >= 1 else "ALREADY APPLIED"
    if kind == "insertAfter":
        if len(paragraphs_exactly(chapter_text, fix["text"])) >= 1:
            return "ALREADY APPLIED"
        anchors = len(paragraphs_exactly(chapter_text, fix["after"]))
        if anchors == 1:
            return "READY"
        return "NOT FOUND (fix by hand)" if anchors == 0 else "FOUND %d TIMES (skipped; fix by hand)" % anchors
    if kind == "deleteParagraph":
        found = len(paragraphs_exactly(chapter_text, fix["text"]))
        if found == 1:
            return "READY"
        return "GONE (already deleted, or the paragraph never matched; check by hand)" if found == 0 else "FOUND %d TIMES (skipped; fix by hand)" % found
    return "UNKNOWN KIND %s (skipped)" % kind


def apply_fix(fix, chapter_text):
    kind = fix.get("kind", "replace")
    if kind == "replace" and fix.get("after"):
        region_start, _ = text_after_anchor(chapter_text, fix["after"])
        region = chapter_text[region_start:]
        find_position = region.find(fix["find"])
        changed_region = region[:find_position] + fix["replace"] + region[find_position + len(fix["find"]):]
        return chapter_text[:region_start] + changed_region
    if kind == "replace":
        return chapter_text.replace(fix["find"], fix["replace"], 1)
    if kind == "replaceAll":
        return chapter_text.replace(fix["find"], fix["replace"])
    blocks = chapter_text.split("\n\n")
    if kind == "insertAfter":
        for block_index in range(len(blocks)):
            if blocks[block_index].strip() == fix["after"].strip():
                blocks.insert(block_index + 1, fix["text"])
                break
    if kind == "deleteParagraph":
        blocks = [block for block in blocks if block.strip() != fix["text"].strip()]
    return "\n\n".join(blocks)


def run(mode, batch_path):
    batch = json.load(open(batch_path, encoding="utf-8"))
    base_folder = os.path.dirname(os.path.abspath(batch_path))
    chapters_folder = os.path.join(base_folder, batch.get("folder", "."))
    backups_folder = os.path.join(base_folder, batch.get("backups", "backups"))
    start_marker = batch.get("startMarker", "")
    end_marker = batch.get("endMarker", "")
    print("=== %s: %s%s ===" % (mode.upper(), batch.get("name", "fixes"), "" if mode == "apply" else " (changes nothing)"))

    fixes_by_doc = {}
    for fix in batch["fixes"]:
        fixes_by_doc.setdefault(fix["doc"], []).append(fix)

    totals = {}
    for doc_name, doc_fixes in fixes_by_doc.items():
        doc_path = os.path.join(chapters_folder, doc_name)
        if not os.path.isfile(doc_path):
            print("NO FILE %s: %d fix(es) skipped" % (doc_path, len(doc_fixes)))
            totals["SKIPPED"] = totals.get("SKIPPED", 0) + len(doc_fixes)
            continue
        original_text = open(doc_path, encoding="utf-8", newline="").read()
        bounds = chapter_bounds(original_text, start_marker, end_marker)
        if bounds is None:
            print("%s: markers not found, %d fix(es) skipped" % (doc_name, len(doc_fixes)))
            totals["SKIPPED"] = totals.get("SKIPPED", 0) + len(doc_fixes)
            continue
        before_chapter = original_text[:bounds[0]]
        chapter_text = original_text[bounds[0]:bounds[1]]
        after_chapter = original_text[bounds[1]:]
        print("--- %s ---" % doc_name)
        changed = 0
        for fix in doc_fixes:
            state = fix_status(fix, chapter_text)
            if state == "READY" and mode == "apply":
                chapter_text = apply_fix(fix, chapter_text)
                changed = changed + 1
                state = "APPLIED"
            print("%s: %s" % (state, fix["id"]))
            key = state.split(" (")[0]
            totals[key] = totals.get(key, 0) + 1
        if changed > 0:
            os.makedirs(backups_folder, exist_ok=True)
            stem, extension = os.path.splitext(doc_name)
            stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            backup_path = os.path.join(backups_folder, "%s_%s%s" % (stem, stamp, extension))
            shutil.copy2(doc_path, backup_path)
            if open(backup_path, encoding="utf-8", newline="").read() != original_text:
                print("BACKUP DID NOT MATCH, so %s was not changed" % doc_name)
                continue
            with open(doc_path, "w", encoding="utf-8", newline="") as output_file:
                output_file.write(before_chapter + chapter_text + after_chapter)
            print("BACKED UP to %s, then saved %d change(s)" % (backup_path, changed))
    print("TOTALS: %s" % json.dumps(totals))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("check", "apply"):
        print(__doc__)
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])

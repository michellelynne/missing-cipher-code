"""Reads the percentages from Claude Code's /usage screen, for people on a Claude subscription.

Usage: python3 tools/plan_usage.py <raw screen capture>

Claude Code has no command that prints plan usage for a script, so tools/measure_plan_usage.sh
opens Claude Code, types /usage, and saves what the screen showed. This script finds the
"Current session" and "Current week" lines in that capture and prints them as JSON, for example:

    {"session_percent": 6, "week_percent": 30, "week_resets": "Nov 13 at 10am (America/New_York)"}

If the /usage screen changes and a number can't be found, its value is null.
"""
import json
import re
import sys
from pathlib import Path

# Terminal color and cursor codes, which the capture is full of.
ESCAPE_CODE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]")
PERCENT_PATTERN = re.compile(r"(\d{1,3})\s*%\s*used")
RESETS_PATTERN = re.compile(r"Resets\s+([^\n\r]+)")


def plain_text(raw_capture):
    text = ESCAPE_CODE_PATTERN.sub(" ", raw_capture)
    text = text.replace("\r", "\n")
    return re.sub(r"[ \t]+", " ", text)


def reading_after(text, label):
    """The first percentage and reset time that follow a label such as "Current week"."""
    label_position = text.rfind(label)
    if label_position == -1:
        return None, None
    following_text = text[label_position:label_position + 600]
    percent_match = PERCENT_PATTERN.search(following_text)
    resets_match = RESETS_PATTERN.search(following_text)
    percent = int(percent_match.group(1)) if percent_match else None
    resets = resets_match.group(1).strip() if resets_match else None
    return percent, resets


def read_usage(raw_capture):
    text = plain_text(raw_capture)
    session_percent, session_resets = reading_after(text, "Current session")
    week_percent, week_resets = reading_after(text, "Current week (all models)")
    if week_percent is None:
        week_percent, week_resets = reading_after(text, "Current week")
    problem = None
    squeezed_text = re.sub(r"\s+", "", text).lower()
    if "selectloginmethod" in squeezed_text or "pastecodehere" in squeezed_text:
        problem = "Claude Code isn't signed in on this computer. Run claude once, sign in, and try again."
    elif "doyoutrust" in squeezed_text:
        problem = "Claude Code is asking whether to trust this folder. Run claude here once, answer it, and try again."
    return {
        "problem": problem,
        "session_percent": session_percent,
        "session_resets": session_resets,
        "week_percent": week_percent,
        "week_resets": week_resets,
    }


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raw_capture = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace")
    print(json.dumps(read_usage(raw_capture)))


if __name__ == "__main__":
    main()

"""Reads Claude subscription usage from Claude Code's /usage screen.

Usage: python3 tools/plan_usage.py           prints your current usage as JSON

tools/run_evals.py uses this to record how much of your plan each eval run uses. Claude Code has
no command that prints plan usage for a script, so this opens Claude Code with `expect` (built
into macOS), types /usage, saves the screen, and reads the "Current session" and "Current week"
percentages from it. Opening Claude Code to read /usage sends nothing to Claude.

If the /usage screen changes and a number can't be found, its value is null. With an API key
instead of a subscription, /usage shows no plan bars and both values are null.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY_FOLDER = Path(__file__).resolve().parent.parent
# Terminal color and cursor codes, which the capture is full of.
ESCAPE_CODE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]")
PERCENT_PATTERN = re.compile(r"(\d{1,3})\s*%\s*used")
RESETS_PATTERN = re.compile(r"Resets\s+([^\n\r]+)")
# Waits a fixed time at each step: the screen is drawn with terminal codes between the words,
# so watching for particular text isn't reliable. Takes about 25 seconds.
EXPECT_SCRIPT = r"""
set timeout 10
log_file -noappend $env(CAPTURE_PATH)
cd $env(REPOSITORY_FOLDER)
spawn -noecho claude
sleep 6
send "/usage"
sleep 1
send "\r"
sleep 6
send "\x1b"
sleep 1
send "/exit\r"
expect {
  eof {}
  timeout { send "\x03"; sleep 1; send "\x03"; expect eof }
}
"""


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
        problem = "Claude Code isn't signed in on this computer. Run claude once and sign in."
    elif "doyoutrust" in squeezed_text:
        problem = "Claude Code is asking whether to trust this folder. Run claude here once and answer it."
    elif week_percent is None:
        problem = "No plan usage on the /usage screen (an API key instead of a subscription, or the screen changed)."
    return {
        "problem": problem,
        "session_percent": session_percent,
        "session_resets": session_resets,
        "week_percent": week_percent,
        "week_resets": week_resets,
    }


def measure():
    """Opens Claude Code, reads /usage, and returns the numbers (or a problem saying why not)."""
    for required_program in ("expect", "claude"):
        if shutil.which(required_program) is None:
            return {"problem": "Needs " + required_program + " to read plan usage, and it isn't installed.",
                    "session_percent": None, "session_resets": None, "week_percent": None, "week_resets": None}
    with tempfile.TemporaryDirectory() as temporary_folder:
        capture_path = Path(temporary_folder) / "usage-screen.txt"
        environment = {"CAPTURE_PATH": str(capture_path), "REPOSITORY_FOLDER": str(REPOSITORY_FOLDER)}
        subprocess.run(["expect", "-c", EXPECT_SCRIPT], env=dict(os.environ, **environment),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, check=False)
        raw_capture = capture_path.read_text(encoding="utf-8", errors="replace") if capture_path.exists() else ""
    return read_usage(raw_capture)


def main():
    if len(sys.argv) == 2:
        print(json.dumps(read_usage(Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace"))))
        return
    print(json.dumps(measure()))


if __name__ == "__main__":
    main()

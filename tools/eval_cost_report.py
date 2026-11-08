"""Turns an eval run into a cost and speed table for the README.

Usage: python3 tools/eval_cost_report.py <aggregate-result.json> [more result files...]

Reads the results `claude plugin eval` writes (aggregate-result.json) and prints a Markdown
table with one row per case: what the case covers, the pace it asked for, and for each arm
(with the skill, without it) the score, the median cost in US dollars, and the median time.
Pass several result files to combine runs; cases with the same name are pooled.
"""
import json
import re
import statistics
import sys
from pathlib import Path

PASS_PATTERN = re.compile(r"^pass(\d+)(?:-(\d+))?")
ARM_LABELS = {"with": "With the skill", "without": "Without"}


def pass_label(case_name):
    pass_match = PASS_PATTERN.match(case_name)
    if pass_match is None:
        return "Setup, fixes, or safety"
    if pass_match.group(2):
        return "Passes " + pass_match.group(1) + " to " + pass_match.group(2)
    return "Pass " + pass_match.group(1)


def pace_label(prompt_text):
    lowered_text = prompt_text.lower()
    if "one pass at a time" in lowered_text:
        return "One pass at a time"
    if "all at once" in lowered_text:
        return "All at once"
    return "Not set"


def collect_runs(result_paths):
    cases = {}
    for result_path in result_paths:
        result = json.loads(Path(result_path).read_text(encoding="utf-8"))
        for case in result["cases"]:
            case_entry = cases.setdefault(case["name"], {"prompt": case.get("promptMarkdown", ""), "arms": {}})
            for arm_name, arm_runs in case["arms"].items():
                completed_runs = [run for run in arm_runs if not run.get("error")]
                case_entry["arms"].setdefault(arm_name, []).extend(completed_runs)
    return cases


def describe_arm(arm_runs):
    if not arm_runs:
        return "no runs"
    mean_score = statistics.mean(run["score"] for run in arm_runs)
    median_cost = statistics.median(run["costUsd"] for run in arm_runs)
    median_seconds = statistics.median(run["durationSeconds"] for run in arm_runs)
    return "{:.0%}, ${:.2f}, {:.0f}s".format(mean_score, median_cost, median_seconds)


def build_table(cases):
    arm_names = [arm_name for arm_name in ARM_LABELS if any(arm_name in case["arms"] for case in cases.values())]
    header_cells = ["Case", "Covers", "Pace"] + [ARM_LABELS[arm_name] + " (score, cost, time)" for arm_name in arm_names]
    lines = ["| " + " | ".join(header_cells) + " |", "|" + "---|" * len(header_cells)]
    for case_name in sorted(cases):
        case = cases[case_name]
        row_cells = ["`" + case_name + "`", pass_label(case_name), pace_label(case["prompt"])]
        row_cells.extend(describe_arm(case["arms"].get(arm_name, [])) for arm_name in arm_names)
        lines.append("| " + " | ".join(row_cells) + " |")
    lines.append("")
    lines.append("Score is the share of checks passed, averaged over runs. Cost and time are medians per run, "
                 "for the run itself (grading not included). Runs that errored are left out.")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    print(build_table(collect_runs(sys.argv[1:])))


if __name__ == "__main__":
    main()

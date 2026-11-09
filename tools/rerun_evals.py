"""Reruns only the eval cases that failed last time, plus any cases added since.

Usage, from the top of the repository:
    python3 tools/rerun_evals.py [--dry-run] [--only failed|new] [--results <aggregate-result.json>] [-- <eval options>]

Examples:
    python3 tools/rerun_evals.py --dry-run
    python3 tools/rerun_evals.py -- --runs 1 --model sonnet
    tools/measure_plan_usage.sh "rerun failures" python3 tools/rerun_evals.py -- --runs 1 --model sonnet

It reads every earlier run in skills/editor/evals/results/, keeps each case's latest result (or
uses only the file you name), and picks:
- failed: a case that scored below 100% with the skill, had a run that errored, or was cut off
  by the cost limit
- new: a case folder in skills/editor/evals/ that isn't in those results (new, or it never
  started because the last run stopped early)

`claude plugin eval` selects one case at a time with --case, so this copies the chosen cases into
a temporary eval folder and runs them together, giving one report. Everything after `--` is passed
to `claude plugin eval`. --scaffold, --allow-tools Write Edit Bash, and --no-publish are added
unless you pass them yourself. Results go to skills/editor/evals/results/<time>-rerun/.
"""
import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPOSITORY_FOLDER = Path(__file__).resolve().parent.parent
SKILL_FOLDER = REPOSITORY_FOLDER / "skills" / "editor"
EVALS_FOLDER = SKILL_FOLDER / "evals"
RESULTS_FOLDER = EVALS_FOLDER / "results"
TEMPORARY_EVAL_FOLDER_NAME = "rerun-evals"
DEFAULT_EVAL_OPTIONS = {
    "--scaffold": ["--scaffold"],
    "--allow-tools": ["--allow-tools", "Write", "Edit", "Bash"],
    "--no-publish": ["--no-publish"],
}


def all_case_names():
    return sorted(folder.name for folder in EVALS_FOLDER.iterdir()
                  if folder.is_dir() and ((folder / "prompt.md").exists() or (folder / "case.yaml").exists()))


def earlier_result_paths():
    result_paths = sorted(RESULTS_FOLDER.glob("*/aggregate-result.json"))
    if not result_paths:
        raise SystemExit("No earlier results in " + str(RESULTS_FOLDER.relative_to(REPOSITORY_FOLDER)) + ". Run the full evals first.")
    return result_paths


def latest_case_results(result_paths):
    """Each case's most recent result, so a rerun of a few cases doesn't hide the others."""
    latest = {}
    for result_path in result_paths:
        for case in json.loads(result_path.read_text(encoding="utf-8"))["cases"]:
            latest[case["name"]] = case
    return latest


def case_needs_rerun(case):
    with_runs = case["arms"].get("with", [])
    if not with_runs:
        return True
    for run in with_runs:
        if run.get("error") or run.get("skippedPaidGraders") or run["score"] < 1:
            return True
    return False


def choose_cases(cases_in_results, include_failed, include_new):
    chosen = []
    for case_name in all_case_names():
        if case_name not in cases_in_results:
            if include_new:
                chosen.append((case_name, "no earlier result: new, or never started"))
        elif include_failed and case_needs_rerun(cases_in_results[case_name]):
            chosen.append((case_name, "failed or didn't finish"))
    return chosen


def eval_options(passed_options):
    options = list(passed_options)
    for option_name, default_option in DEFAULT_EVAL_OPTIONS.items():
        if option_name not in options:
            options.extend(default_option)
    if "--output-dir" not in options:
        run_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        options.extend(["--output-dir", str(RESULTS_FOLDER / (run_time + "-rerun"))])
    return options


def main():
    arguments = sys.argv[1:]
    passed_options = []
    if "--" in arguments:
        separator_index = arguments.index("--")
        passed_options = arguments[separator_index + 1:]
        arguments = arguments[:separator_index]
    parser = argparse.ArgumentParser(description="Rerun failed and new eval cases.")
    parser.add_argument("--results", help="One aggregate-result.json to compare against (default: every earlier run, latest result per case)")
    parser.add_argument("--only", choices=["failed", "new"], help="Rerun only failed cases, or only new ones")
    parser.add_argument("--dry-run", action="store_true", help="List the cases without running them")
    settings = parser.parse_args(arguments)

    result_paths = [Path(settings.results)] if settings.results else earlier_result_paths()
    chosen = choose_cases(latest_case_results(result_paths), settings.only != "new", settings.only != "failed")
    print("Compared with each case's latest result in", len(result_paths), "earlier run(s)")
    if not chosen:
        print("Nothing to rerun: every case passed and there are no new cases.")
        return
    for case_name, reason in chosen:
        print("  " + case_name + " (" + reason + ")")
    if settings.dry_run:
        return

    temporary_folder = SKILL_FOLDER / TEMPORARY_EVAL_FOLDER_NAME
    if temporary_folder.exists():
        shutil.rmtree(temporary_folder)
    temporary_folder.mkdir()
    try:
        for case_name, _ in chosen:
            shutil.copytree(EVALS_FOLDER / case_name, temporary_folder / case_name)
        command = ["claude", "plugin", "eval", str(SKILL_FOLDER.relative_to(REPOSITORY_FOLDER)),
                   "--eval-dir", TEMPORARY_EVAL_FOLDER_NAME] + eval_options(passed_options)
        print("Running:", " ".join(command))
        completed_run = subprocess.run(command, cwd=REPOSITORY_FOLDER, check=False)
    finally:
        shutil.rmtree(temporary_folder, ignore_errors=True)
    sys.exit(completed_run.returncode)


if __name__ == "__main__":
    main()

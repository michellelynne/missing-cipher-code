"""Runs the Editor's evals and, with --summary, writes the results page when they finish.

Usage, from the top of the repository:
    python3 tools/run_evals.py [--summary] [--rerun | --only failed|new] [--dry-run] [-- <eval options>]

Examples:
    python3 tools/run_evals.py --summary                                  every case, 3 runs each
    python3 tools/run_evals.py --summary -- --runs 1 --model sonnet       every case, once, lighter
    python3 tools/run_evals.py --rerun --summary -- --runs 1              only failed and new cases
    python3 tools/run_evals.py --rerun --dry-run                          list them without running

Choosing cases:
    (default)       every case in skills/editor/evals/
    --rerun         cases that failed last time, plus cases with no result yet. "Failed" means
                    the case scored below 100% with the skill, a run errored, or the cost limit
                    cut it off. Each case's latest result across earlier runs is used, so a case
                    that failed and then passed on a rerun drops off the list.
    --only failed   (or new) narrows --rerun to one of the two
    --results FILE  compare against one results file instead of every earlier run

--summary writes skills/editor/evals/results/eval-summary.html from every run so far (each case's
latest result) and prints where it is, even if some runs failed.

Everything after `--` goes to `claude plugin eval`. --scaffold, --allow-tools Write Edit Bash, and
--no-publish are added unless you pass them yourself. Results go to
skills/editor/evals/results/<time>/.
"""
import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

import eval_summary

REPOSITORY_FOLDER = Path(__file__).resolve().parent.parent
SKILL_FOLDER = REPOSITORY_FOLDER / "skills" / "editor"
EVALS_FOLDER = SKILL_FOLDER / "evals"
RESULTS_FOLDER = EVALS_FOLDER / "results"
SUMMARY_PATH = RESULTS_FOLDER / "eval-summary.html"
# `claude plugin eval` selects only one case at a time with --case, so a rerun copies the chosen
# cases into this folder and points --eval-dir at it.
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
    return sorted(RESULTS_FOLDER.glob("*/aggregate-result.json"))


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


def choose_rerun_cases(cases_in_results, include_failed, include_new):
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
        options.extend(["--output-dir", str(RESULTS_FOLDER / run_time)])
    return options


def run_eval_command(command):
    print("Running:", " ".join(command))
    return subprocess.run(command, cwd=REPOSITORY_FOLDER, check=False).returncode


def run_every_case(passed_options):
    command = ["claude", "plugin", "eval", str(SKILL_FOLDER.relative_to(REPOSITORY_FOLDER))] + eval_options(passed_options)
    return run_eval_command(command)


def run_chosen_cases(chosen, passed_options):
    temporary_folder = SKILL_FOLDER / TEMPORARY_EVAL_FOLDER_NAME
    if temporary_folder.exists():
        shutil.rmtree(temporary_folder)
    temporary_folder.mkdir()
    try:
        for case_name, _ in chosen:
            shutil.copytree(EVALS_FOLDER / case_name, temporary_folder / case_name)
        command = ["claude", "plugin", "eval", str(SKILL_FOLDER.relative_to(REPOSITORY_FOLDER)),
                   "--eval-dir", TEMPORARY_EVAL_FOLDER_NAME] + eval_options(passed_options)
        return run_eval_command(command)
    finally:
        shutil.rmtree(temporary_folder, ignore_errors=True)


def write_summary():
    result_paths = earlier_result_paths()
    if not result_paths:
        print("No results to summarize yet.")
        return
    result_files = [json.loads(result_path.read_text(encoding="utf-8")) for result_path in result_paths]
    result_files.sort(key=lambda result: result.get("startedAt", ""))
    SUMMARY_PATH.write_text(eval_summary.build_page(result_files), encoding="utf-8")
    print("Results page:", SUMMARY_PATH.relative_to(REPOSITORY_FOLDER), "(" + str(len(result_paths)) + " run(s), latest result per case)")


def main():
    arguments = sys.argv[1:]
    passed_options = []
    if "--" in arguments:
        separator_index = arguments.index("--")
        passed_options = arguments[separator_index + 1:]
        arguments = arguments[:separator_index]
    parser = argparse.ArgumentParser(description="Run the Editor evals.", epilog="Run with --help-full for every detail.")
    parser.add_argument("--summary", action="store_true", help="Write the results page when the run finishes")
    parser.add_argument("--rerun", action="store_true", help="Run only cases that failed last time, plus new ones")
    parser.add_argument("--only", choices=["failed", "new"], help="With --rerun, only failed cases or only new ones")
    parser.add_argument("--results", help="One aggregate-result.json to compare against (default: every earlier run)")
    parser.add_argument("--dry-run", action="store_true", help="List the cases without running them")
    parser.add_argument("--help-full", action="store_true", help="Show the full explanation")
    settings = parser.parse_args(arguments)
    if settings.help_full:
        print(__doc__)
        return

    rerun = settings.rerun or settings.only is not None or settings.results is not None
    if rerun:
        result_paths = [Path(settings.results)] if settings.results else earlier_result_paths()
        if not result_paths:
            raise SystemExit("No earlier results to compare against. Run every case first: python3 tools/run_evals.py --summary")
        chosen = choose_rerun_cases(latest_case_results(result_paths), settings.only != "new", settings.only != "failed")
        print("Compared with each case's latest result in", len(result_paths), "earlier run(s)")
        if not chosen:
            print("Nothing to rerun: every case passed and there are no new cases.")
            return
    else:
        chosen = [(case_name, "every case") for case_name in all_case_names()]
    for case_name, reason in chosen:
        print("  " + case_name + ("" if not rerun else " (" + reason + ")"))
    if settings.dry_run:
        return

    exit_status = run_chosen_cases(chosen, passed_options) if rerun else run_every_case(passed_options)
    if settings.summary:
        write_summary()
    sys.exit(exit_status)


if __name__ == "__main__":
    main()

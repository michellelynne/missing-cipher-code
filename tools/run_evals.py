"""Runs the Editor's evals, records how much of your Claude plan they used, and writes a results page.

Usage, from the top of the repository:
    python3 tools/run_evals.py [--rerun | --only failed|new] [--dry-run] [--no-usage] [-- <eval options>]

Examples:
    python3 tools/run_evals.py                                  every case, 3 runs each
    python3 tools/run_evals.py -- --runs 1 --model sonnet       every case, once, lighter on usage
    python3 tools/run_evals.py --rerun -- --runs 1              only failed and new cases
    python3 tools/run_evals.py --rerun --dry-run                list them without running

Choosing cases:
    (default)       every case in skills/editor/evals/
    --rerun         cases that failed last time, plus cases with no result yet. "Failed" means
                    the case scored below 100% with the skill, a run errored, or the cost limit
                    cut it off. Each case's latest result across earlier runs is used, so a case
                    that failed and then passed on a rerun drops off the list.
    --only failed   (or new) narrows --rerun to one of the two
    --results FILE  compare against one results file instead of every earlier run

Plan usage: on a Claude subscription, the script reads Claude Code's /usage screen before and
after the run (about a minute in all) and saves the change with the run's results. Needs
`expect`, which comes with macOS. Don't use Claude for anything else during the run, since that
counts too. --no-usage skips it.

When the run finishes, it writes skills/editor/evals/results/eval-summary.html from every run so
far: scores with and without the skill, failed checks, each run's usage, tokens, cost, and time,
and estimates of what a full run takes. --no-summary skips it. --plan "Claude Max 5x" (or the
EVAL_PLAN_NAME environment variable) names your plan on the page.

Everything after `--` goes to `claude plugin eval`. --scaffold, --allow-tools Write Edit Bash, and
--no-publish are added unless you pass them yourself. Results go to
skills/editor/evals/results/<time>/.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import eval_summary
import plan_usage

REPOSITORY_FOLDER = Path(__file__).resolve().parent.parent
SKILL_FOLDER = REPOSITORY_FOLDER / "skills" / "editor"
EVALS_FOLDER = SKILL_FOLDER / "evals"
RESULTS_FOLDER = EVALS_FOLDER / "results"
SUMMARY_PATH = RESULTS_FOLDER / "eval-summary.html"
USAGE_FILE_NAME = "plan-usage.json"
# /usage can lag a little behind the work, so the second reading waits this long.
USAGE_SETTLE_SECONDS = int(os.environ.get("EVAL_USAGE_SETTLE_SECONDS", "60"))
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
    """The options for claude plugin eval, and the folder its results will go to."""
    options = list(passed_options)
    for option_name, default_option in DEFAULT_EVAL_OPTIONS.items():
        if option_name not in options:
            options.extend(default_option)
    if "--output-dir" in options:
        output_folder = Path(options[options.index("--output-dir") + 1])
    else:
        run_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
        output_folder = RESULTS_FOLDER / run_time
        options.extend(["--output-dir", str(output_folder)])
    return options, output_folder


def run_eval_command(command):
    print("Running:", " ".join(command))
    return subprocess.run(command, cwd=REPOSITORY_FOLDER, check=False).returncode


def eval_command(options, eval_folder_name=None):
    command = ["claude", "plugin", "eval", str(SKILL_FOLDER.relative_to(REPOSITORY_FOLDER))]
    if eval_folder_name:
        command.extend(["--eval-dir", eval_folder_name])
    return command + options


def run_cases(chosen, rerun, options):
    if not rerun:
        return run_eval_command(eval_command(options))
    temporary_folder = SKILL_FOLDER / TEMPORARY_EVAL_FOLDER_NAME
    if temporary_folder.exists():
        shutil.rmtree(temporary_folder)
    temporary_folder.mkdir()
    try:
        for case_name, _ in chosen:
            shutil.copytree(EVALS_FOLDER / case_name, temporary_folder / case_name)
        return run_eval_command(eval_command(options, TEMPORARY_EVAL_FOLDER_NAME))
    finally:
        shutil.rmtree(temporary_folder, ignore_errors=True)


def read_plan_usage(moment):
    print("Reading plan usage " + moment + " the run (about 25 seconds)...")
    usage = plan_usage.measure()
    if usage["problem"]:
        print("  Skipping plan usage: " + usage["problem"])
        return None
    print("  Week {}%, current session {}%".format(usage["week_percent"], usage["session_percent"]))
    return usage


def save_plan_usage(output_folder, usage_before, usage_after, run_minutes):
    if usage_before is None or usage_after is None or not output_folder.exists():
        return
    record = {"before": usage_before, "after": usage_after, "minutes": run_minutes}
    (output_folder / USAGE_FILE_NAME).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    week_change = usage_after["week_percent"] - usage_before["week_percent"]
    session_change = (usage_after["session_percent"] or 0) - (usage_before["session_percent"] or 0)
    print("Plan usage: {:+d} points of your week, {:+d} points of the current 5-hour session".format(week_change, session_change))


def write_summary(plan):
    if not earlier_result_paths():
        print("No results to summarize yet.")
        return
    SUMMARY_PATH.write_text(eval_summary.build_page(eval_summary.load_runs(RESULTS_FOLDER), plan), encoding="utf-8")
    print("Results page:", SUMMARY_PATH.relative_to(REPOSITORY_FOLDER))


def main():
    arguments = sys.argv[1:]
    passed_options = []
    if "--" in arguments:
        separator_index = arguments.index("--")
        passed_options = arguments[separator_index + 1:]
        arguments = arguments[:separator_index]
    parser = argparse.ArgumentParser(description="Run the Editor evals.", epilog="Run with --help-full for every detail.")
    parser.add_argument("--no-usage", action="store_true", help="Don't read /usage before and after the run")
    parser.add_argument("--no-summary", action="store_true", help="Don't write the results page")
    parser.add_argument("--plan", default=os.environ.get("EVAL_PLAN_NAME", eval_summary.DEFAULT_PLAN),
                        help='Your Claude plan, shown on the results page, such as "Claude Max 5x" (or set EVAL_PLAN_NAME)')
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
            raise SystemExit("No earlier results to compare against. Run every case first: python3 tools/run_evals.py")
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

    options, output_folder = eval_options(passed_options)
    usage_before = None if settings.no_usage else read_plan_usage("before")
    start_seconds = time.time()
    exit_status = run_cases(chosen, rerun, options)
    run_minutes = round((time.time() - start_seconds) / 60)
    if usage_before is not None:
        print("Waiting {} seconds for usage to catch up...".format(USAGE_SETTLE_SECONDS))
        time.sleep(USAGE_SETTLE_SECONDS)
        save_plan_usage(output_folder, usage_before, read_plan_usage("after"), run_minutes)
    if not settings.no_summary:
        write_summary(settings.plan)
    sys.exit(exit_status)


if __name__ == "__main__":
    main()

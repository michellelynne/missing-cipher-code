"""Turns eval results into a short, readable HTML page anyone can follow.

Usage: python3 tools/eval_summary.py [<aggregate-result.json> ...] [--plan "Claude Max 5x"] [--output page.html]

tools/run_evals.py writes this page after every run, so you rarely need to run this yourself.
With no files, it reads every run in skills/editor/evals/results/ and writes eval-summary.html
there.

The page covers what each test checks, how much the skill helps, which checks fail, each run's
plan usage, tokens, cost, and time, and estimates of what a full run takes. Plan usage comes from
the plan-usage.json that run_evals.py saves with each run (or from an older plan-usage.csv in the
results folder). When several runs include a case, its most recent result is used.
"""
import csv
import datetime
import html
import json
import re
import statistics
import sys
from pathlib import Path

REPOSITORY_FOLDER = Path(__file__).resolve().parent.parent
EVALS_FOLDER = REPOSITORY_FOLDER / "skills" / "editor" / "evals"
RESULTS_FOLDER = EVALS_FOLDER / "results"
USAGE_FILE_NAME = "plan-usage.json"
OLD_USAGE_LOG_NAME = "plan-usage.csv"
# The plan the usage was measured on. Set it with --plan, for example --plan "Claude Max 5x".
DEFAULT_PLAN = "Claude Max"
# The share of a 5-hour session above which an estimate warns that a run may hit the limit.
SESSION_WARNING_POINTS = 80
WITH_ARM = "with"
# Words that should keep their capitals, or read better spelled out, in case and check names.
NAME_WORDS = {"google": "Google", "docs": "Docs", "word": "Word", "scrivener": "Scrivener", "pov": "POV",
              "pass0": "Pass 0", "pass1": "Pass 1", "pass4": "Passes 4 and", "crossref": "cross-reference"}


def escape(text):
    return html.escape(str(text))


def readable_name(slug):
    words = slug.split("-")
    if words and words[0].isdigit():
        words = words[1:]
    sentence = " ".join(NAME_WORDS.get(word, word) for word in words)
    return sentence[0].upper() + sentence[1:] if sentence else sentence


def all_case_names():
    return sorted(folder.name for folder in EVALS_FOLDER.iterdir()
                  if folder.is_dir() and ((folder / "prompt.md").exists() or (folder / "case.yaml").exists()))


def case_description(case_name):
    """The first sentence of the case's expected outcome, from its case.yaml."""
    case_file = EVALS_FOLDER / case_name / "case.yaml"
    if not case_file.exists():
        return ""
    lines = case_file.read_text(encoding="utf-8").splitlines()
    collected = []
    collecting = False
    for line_text in lines:
        if line_text.startswith("expected_outcome:"):
            collecting = True
            continue
        if collecting:
            if line_text.startswith("  "):
                collected.append(line_text.strip())
            else:
                break
    outcome = " ".join(collected)
    first_sentence = re.split(r"(?<=\.)\s", outcome, maxsplit=1)[0]
    return first_sentence


def session_events(run):
    """The session record of one run. Graders that read the trace carry it as their evidence."""
    for grader in run.get("graders") or []:
        evidence = grader.get("evidence", "")
        if not evidence.startswith("{"):
            continue
        events = []
        for line_text in evidence.splitlines():
            try:
                events.append(json.loads(line_text))
            except json.JSONDecodeError:
                continue
        if any(event.get("type") in ("system", "result") for event in events):
            return events
    return []


def run_tokens(run):
    """Tokens one run used, read from its session record. Returns 0 when the record has no usage."""
    for event in session_events(run):
        if event.get("type") == "result" and "usage" in event:
            usage = event["usage"]
            return (usage.get("input_tokens", 0) + usage.get("output_tokens", 0) +
                    usage.get("cache_read_input_tokens", 0) + usage.get("cache_creation_input_tokens", 0))
    return 0


def run_model(run):
    for event in session_events(run):
        if event.get("type") == "system" and event.get("model"):
            return event["model"]
    return None


def tokens_text(token_count):
    if token_count == 0:
        return "n/a"
    if token_count >= 1000000:
        return "{:.1f}M".format(token_count / 1000000)
    return "{:.0f}K".format(token_count / 1000)


def percent(value):
    return "n/a" if value is None else "{:.0%}".format(value)


def started_time(result):
    started_text = result.get("startedAt", "")
    try:
        return datetime.datetime.fromisoformat(started_text.replace("Z", "+00:00"))
    except ValueError:
        return None


def old_usage_rows(results_folder):
    """Rows from plan-usage.csv, the log an earlier version of the usage check wrote."""
    log_path = results_folder / OLD_USAGE_LOG_NAME
    if not log_path.exists():
        return []
    rows = []
    with open(log_path, encoding="utf-8", newline="") as log_file:
        for row in csv.DictReader(log_file):
            try:
                finished_local = datetime.datetime.strptime(row["date"], "%Y-%m-%d %H:%M").astimezone()
                rows.append({"finished": finished_local, "minutes": int(row["minutes"] or 0), "usage": {
                    "before": {"week_percent": int(row["week_before"]), "session_percent": int(row["session_before"] or 0)},
                    "after": {"week_percent": int(row["week_after"]), "session_percent": int(row["session_after"] or 0)},
                    "minutes": int(row["minutes"] or 0)}})
            except (KeyError, ValueError):
                continue
    return rows


def matching_old_usage(result, rows):
    """The old log row written when this run finished, if there is one."""
    started = started_time(result)
    if started is None:
        return None
    finished = started + datetime.timedelta(seconds=result.get("durationSeconds", 0))
    for row in rows:
        if started <= row["finished"] <= finished + datetime.timedelta(minutes=10):
            return row["usage"]
    return None


def load_runs(results_folder=RESULTS_FOLDER, result_paths=None):
    """Every run's results and plan usage, oldest first."""
    result_paths = result_paths or sorted(results_folder.glob("*/aggregate-result.json"))
    old_rows = old_usage_rows(results_folder)
    runs = []
    for result_path in result_paths:
        result = json.loads(result_path.read_text(encoding="utf-8"))
        usage_path = result_path.with_name(USAGE_FILE_NAME)
        usage = json.loads(usage_path.read_text(encoding="utf-8")) if usage_path.exists() else matching_old_usage(result, old_rows)
        runs.append({"result": result, "usage": usage, "folder": result_path.parent})
    runs.sort(key=lambda run: run["result"].get("startedAt", ""))
    return runs


def run_sessions(result):
    """Claude Code sessions that actually started in a run, with and without the skill."""
    return [run for case in result["cases"] for runs in case["arms"].values() for run in runs
            if run.get("turns", 0) > 0 or run.get("costUsd", 0) > 0]


def describe_run(run):
    result = run["result"]
    sessions = run_sessions(result)
    models = sorted({model for model in (run_model(session) for session in sessions) if model})
    runs_per_case = max([len(case["arms"].get("with", [])) for case in result["cases"]] or [0])
    usage = run["usage"]
    week_change = session_change = None
    if usage and usage.get("before") and usage.get("after"):
        week_change = usage["after"]["week_percent"] - usage["before"]["week_percent"]
        session_change = (usage["after"].get("session_percent") or 0) - (usage["before"].get("session_percent") or 0)
        if session_change < 0:
            session_change = None
    started = started_time(result)
    return {
        "started": started.astimezone().strftime("%Y-%m-%d %H:%M") if started else "",
        "cases": len(result["cases"]),
        "runs_per_case": str(runs_per_case),
        "models": models,
        "sessions": len(sessions),
        "minutes": round(result.get("durationSeconds", 0) / 60),
        "tokens": sum(run_tokens(session) for session in sessions),
        "cost": result.get("costUsd", 0),
        "week_change": week_change,
        "session_change": session_change,
    }


def short_model_name(model):
    for family in ("opus", "sonnet", "haiku"):
        if family in model:
            return family.capitalize()
    return model


def estimates(described_runs, case_count):
    """Tokens, cost, and plan usage per session for each model, and what full runs would take.

    Plan usage is measured only on some runs. For a model with no measured run, usage is scaled
    from the measured model by cost per session, since plan limits track how much work a model
    does; those rows are marked as scaled.
    """
    by_model = {}
    for described in described_runs:
        if len(described["models"]) != 1 or described["sessions"] == 0:
            continue
        totals = by_model.setdefault(described["models"][0], {"sessions": 0, "tokens": 0, "cost": 0, "usage_sessions": 0,
                                                             "week_points": 0, "session_points": 0, "session_sessions": 0,
                                                             "usage_cost": 0})
        totals["sessions"] = totals["sessions"] + described["sessions"]
        totals["tokens"] = totals["tokens"] + described["tokens"]
        totals["cost"] = totals["cost"] + described["cost"]
        if described["week_change"] is not None:
            totals["usage_sessions"] = totals["usage_sessions"] + described["sessions"]
            totals["usage_cost"] = totals["usage_cost"] + described["cost"]
            totals["week_points"] = totals["week_points"] + described["week_change"]
        if described["session_change"] is not None:
            totals["session_sessions"] = totals["session_sessions"] + described["sessions"]
            totals["session_points"] = totals["session_points"] + described["session_change"]

    measured_models = [model for model, totals in by_model.items() if totals["usage_sessions"] and totals["usage_cost"]]
    reference_model = max(measured_models, key=lambda model: by_model[model]["usage_sessions"]) if measured_models else None
    rows = []
    for model, totals in sorted(by_model.items()):
        tokens_each = totals["tokens"] / totals["sessions"]
        cost_each = totals["cost"] / totals["sessions"]
        week_each = totals["week_points"] / totals["usage_sessions"] if totals["usage_sessions"] else None
        session_each = totals["session_points"] / totals["session_sessions"] if totals["session_sessions"] else None
        basis = "measured"
        if week_each is None and reference_model is not None:
            reference = by_model[reference_model]
            reference_cost_each = reference["usage_cost"] / reference["usage_sessions"]
            scale = cost_each / reference_cost_each
            week_each = reference["week_points"] / reference["usage_sessions"] * scale
            if reference["session_sessions"]:
                session_each = reference["session_points"] / reference["session_sessions"] * scale
            basis = "scaled from " + short_model_name(reference_model) + " by cost per session (x{:.1f})".format(scale)
        for label, runs_per_case in (("Every case once", 1), ("Every case 3 times (the default)", 3)):
            sessions = case_count * 2 * runs_per_case
            rows.append({"model": model, "label": label, "sessions": sessions, "tokens": tokens_each * sessions,
                         "cost": cost_each * sessions,
                         "week": None if week_each is None else week_each * sessions,
                         "session": None if session_each is None else session_each * sessions,
                         "basis": basis})
    return rows


def points_text(value):
    return "not measured" if value is None else "about {:.0f}".format(value) if value >= 1 else "under 1"


def completed(runs):
    return [run for run in runs if not run.get("error") and not run.get("skippedPaidGraders")]


def mean_score(runs):
    finished_runs = completed(runs)
    if not finished_runs:
        return None
    return statistics.mean(run["score"] for run in finished_runs)


def grader_results(runs, grader_name):
    results = []
    for run in completed(runs):
        for grader in run.get("graders", []):
            if grader["name"] == grader_name and grader.get("scored", True):
                results.append(grader)
    return results


def latest_cases(result_files):
    """Each case's most recent result across the files, oldest file first."""
    latest = {}
    for result in result_files:
        for case in result["cases"]:
            latest[case["name"]] = case
    return [latest[case_name] for case_name in sorted(latest)]


def summarize_case(case):
    arms = case["arms"]
    baseline_names = [arm_name for arm_name in arms if arm_name != WITH_ARM]
    with_runs = arms.get(WITH_ARM, [])
    baseline_runs = arms.get(baseline_names[0], []) if baseline_names else []
    with_score = mean_score(with_runs)
    baseline_score = mean_score(baseline_runs)
    checks = []
    for grader in case["graders"]:
        with_results = grader_results(with_runs, grader["name"])
        baseline_results = grader_results(baseline_runs, grader["name"])
        reasons = [result.get("explanation", "") for result in with_results if not result["passed"]]
        checks.append({
            "statement": grader.get("graderMarkdown") or grader.get("config", {}).get("criteria", ""),
            "with_passed": sum(1 for result in with_results if result["passed"]),
            "with_total": len(with_results),
            "baseline_passed": sum(1 for result in baseline_results if result["passed"]),
            "baseline_total": len(baseline_results),
            # "judge votes: FAIL FAIL FAIL" says nothing a reader can use, so only real explanations are shown.
            "reasons": [reason for reason in reasons if reason and not reason.startswith("judge votes")],
        })
    all_runs = with_runs + baseline_runs
    return {
        "name": case["name"],
        "description": case_description(case["name"]),
        "with_score": with_score,
        "baseline_score": baseline_score,
        "difference": None if with_score is None or baseline_score is None else with_score - baseline_score,
        "with_runs": len(completed(with_runs)),
        "baseline_runs": len(completed(baseline_runs)),
        "unfinished_runs": len(all_runs) - len(completed(all_runs)),
        "cost": sum(run.get("costUsd", 0) for run in all_runs),
        "tokens": sum(run_tokens(run) for run in all_runs),
        "models": sorted({model for model in (run_model(run) for run in all_runs) if model}),
        "checks": checks,
    }


def score_bar(score, color):
    if score is None:
        return '<span class="muted">not run</span>'
    return ('<div class="bar"><div class="fill" style="width:' + str(round(score * 100)) + '%;background:' + color + '"></div></div>'
            '<span class="value">' + percent(score) + "</span>")


def pass_count_text(passed, total):
    if total == 0:
        return "not run"
    return str(passed) + " of " + str(total)


def build_page(runs, plan=DEFAULT_PLAN):
    result_files = [run["result"] for run in runs]
    described_runs = [describe_run(run) for run in runs]
    cases = [summarize_case(case) for case in latest_cases(result_files)]
    with_scores = [case["with_score"] for case in cases if case["with_score"] is not None]
    baseline_scores = [case["baseline_score"] for case in cases if case["baseline_score"] is not None]
    differences = [case["difference"] for case in cases if case["difference"] is not None]
    models = sorted({model for described in described_runs for model in described["models"]})
    total_tokens = sum(described["tokens"] for described in described_runs)
    total_cost = sum(described["cost"] for described in described_runs)
    total_sessions = sum(described["sessions"] for described in described_runs)
    run_dates = sorted({result.get("startedAt", "")[:10] for result in result_files if result.get("startedAt")})
    unfinished_total = sum(case["unfinished_runs"] for case in cases)

    parts = ["<h1>Editor eval results</h1>"]
    parts.append('<p class="muted">' + str(len(cases)) + " test cases &middot; " + str(len(described_runs)) + " run(s) on " +
                 escape(", ".join(run_dates)) + " &middot; " + escape(", ".join(short_model_name(model) for model in models) or "model not recorded") +
                 " &middot; " + str(total_sessions) + " sessions, " + tokens_text(total_tokens) +
                 " tokens (${:.2f} at API prices) in all</p>".format(total_cost))

    parts.append("""<div class="explain"><strong>How to read this page.</strong> Each test case gives the Editor a
realistic request, such as &ldquo;review chapter 3,&rdquo; with sample files that have problems planted on purpose.
Claude does the task once with the Editor skill and once without it, and a second model checks the
result against a list of specific statements, such as &ldquo;asks setup questions before reviewing.&rdquo;
A score is the share of those checks that passed. <em>Adds</em> is the score with the skill minus the
score without it: what the skill contributes beyond what the model already does.</div>""")
    if unfinished_total:
        parts.append('<p class="notice">' + str(unfinished_total) + " run(s) errored or were stopped by the cost limit. "
                     "They are left out of the scores. Rerun them with <code>python3 tools/run_evals.py --rerun</code>.</p>")

    average_difference = statistics.mean(differences) if differences else None
    parts.append('<div class="totals">')
    parts.append('<div><span class="big">' + percent(statistics.mean(with_scores) if with_scores else None) + "</span>of checks passed with the Editor</div>")
    parts.append('<div><span class="big">' + percent(statistics.mean(baseline_scores) if baseline_scores else None) + "</span>passed without it</div>")
    parts.append('<div><span class="big">' + ("n/a" if average_difference is None else "{:+.0f}".format(average_difference * 100)) +
                 "</span>points the Editor adds, on average</div>")
    parts.append("</div>")

    parts.append("<h2>Each test case</h2><table><tr><th>Test case</th><th>With the Editor</th><th>Without</th><th>Adds</th>"
                 "<th>Runs<br>with / without</th><th>Tokens</th></tr>")
    for case in cases:
        difference_text = "n/a" if case["difference"] is None else "{:+.0f}".format(case["difference"] * 100)
        description = '<div class="muted small">' + escape(case["description"]) + "</div>" if case["description"] else ""
        parts.append("<tr><td><strong>" + escape(readable_name(case["name"])) + "</strong>" + description + "</td><td>" +
                     score_bar(case["with_score"], "#177E89") + "</td><td>" + score_bar(case["baseline_score"], "#9aa5ad") +
                     "</td><td>" + difference_text + '</td><td class="value">' + str(case["with_runs"]) + " / " + str(case["baseline_runs"]) +
                     "</td><td>" + tokens_text(case["tokens"]) + "</td></tr>")
    parts.append("</table>")
    parts.append('<p class="muted small">Tokens: everything the runs read and wrote, '
                 "for both. On a Claude subscription, runs count toward your plan&rsquo;s usage limits instead of being billed.</p>")

    parts.append("<h2>Runs and plan usage</h2><table><tr><th>Started</th><th>What ran</th><th>Sessions</th><th>Minutes</th>"
                 "<th>Tokens</th><th>At API prices</th><th>Weekly limit</th><th>5-hour session</th></tr>")
    for run_index, described in enumerate(described_runs):
        run_folder = runs[run_index].get("folder")
        what_ran = (str(described["cases"]) + " cases &times; " + described["runs_per_case"] + " run(s), " +
                    escape(", ".join(short_model_name(model) for model in described["models"]) or "model not recorded"))
        week_text = "&mdash;" if described["week_change"] is None else "{:+d} points".format(described["week_change"])
        session_text = "&mdash;" if described["session_change"] is None else "{:+d} points".format(described["session_change"])
        report_link = ""
        if run_folder is not None and (run_folder / "report.html").exists():
            report_link = ' <a href="' + escape(run_folder.name) + '/report.html">detailed report</a>'
        parts.append('<tr><td class="value">' + escape(described["started"]) + report_link + "</td><td>" + what_ran + "</td><td>" +
                     str(described["sessions"]) + "</td><td>" + str(described["minutes"]) + "</td><td>" +
                     tokens_text(described["tokens"]) + "</td><td>${:.2f}".format(described["cost"]) + "</td><td>" +
                     week_text + "</td><td>" + session_text + "</td></tr>")
    parts.append("</table>")
    parts.append('<p class="muted small">A session is one Claude Code conversation: one case, run once, with or without '
                 "the Editor. Weekly limit and 5-hour session show how much of a Claude subscription the run used, read from "
                 "<code>/usage</code> before and after; &mdash; means it wasn&rsquo;t measured (an API key, or "
                 "<code>--no-usage</code>). <code>/usage</code> shows whole percentages, so small changes are rough. "
                 "At API prices is what the same run would cost with an API key; on a subscription it isn&rsquo;t a charge.</p>")

    estimate_rows = estimates(described_runs, len(all_case_names()))
    if estimate_rows:
        parts.append("<h2>What a run takes (estimates)</h2>"
                     '<p class="muted small">For all ' + str(len(all_case_names())) + " cases, with and without the Editor, on "
                     + escape(plan) + ". Points are percentage points of the plan&rsquo;s weekly limit and of one 5-hour "
                     "session.</p><table><tr><th>Model</th><th>Run</th><th>Sessions</th><th>Tokens</th><th>At API prices</th>"
                     "<th>Weekly limit</th><th>5-hour session</th></tr>")
        for row in estimate_rows:
            session_text = points_text(row["session"]) + ("" if row["session"] is None else " points")
            if row["session"] is not None and row["session"] >= SESSION_WARNING_POINTS:
                session_text = session_text + ' <span class="warn">' + ("more than one session; " if row["session"] > 100 else "may hit the limit; ") + "split it with --rerun or start in a fresh session</span>"
            parts.append("<tr><td>" + escape(short_model_name(row["model"])) + "</td><td>" + escape(row["label"]) + "</td><td>" +
                         str(row["sessions"]) + "</td><td>" + tokens_text(row["tokens"]) + "</td><td>${:.0f}".format(row["cost"]) +
                         "</td><td>" + points_text(row["week"]) + ("" if row["week"] is None else " points") + "</td><td>" +
                         session_text + "</td></tr>")
        parts.append("</table>")
        bases = sorted({short_model_name(row["model"]) + ": " + row["basis"] for row in estimate_rows})
        parts.append('<p class="muted small">How these are estimated: tokens and cost come from the sessions each model has '
                     "run so far. Plan usage per session is " + escape("; ".join(bases)) + ". Plan limits track how much work "
                     "a model does, so a model that costs more per session uses more of the plan; that scaling is an "
                     "estimate until a run on that model is measured. <code>/usage</code> shows whole percentages, so "
                     "every plan figure is approximate.</p>")
        parts.append('<div class="explain"><strong>About the plan.</strong> These numbers were measured on ' + escape(plan) +
                     ". Claude&rsquo;s paid plans share one usage pool between the Claude apps and Claude Code, with a limit "
                     "per 5-hour session and a weekly limit. Max comes in two tiers: Max 5x ($100 a month) gives five times "
                     "Pro&rsquo;s usage per session, and Max 20x ($200 a month) gives twenty times. So a run that uses 10 "
                     "points of a 5-hour session on Max 5x would use about 50 on Pro and about 2.5 on Max 20x. The weekly "
                     "limits don&rsquo;t scale by exactly the same factors, so treat weekly figures on other plans as rough. "
                     "With an API key instead of a plan, runs are billed at the API prices shown.</div>")

    parts.append("<h2>Checks that didn&rsquo;t always pass with the Editor</h2>")
    any_failures = False
    for case in cases:
        failing_checks = [check for check in case["checks"] if check["with_total"] and check["with_passed"] < check["with_total"]]
        if not failing_checks:
            continue
        any_failures = True
        parts.append("<h3>" + escape(readable_name(case["name"])) + "</h3>")
        for check in failing_checks:
            parts.append('<div class="check"><p>' + escape(check["statement"]) + "</p>")
            parts.append('<p class="muted small">Passed ' + pass_count_text(check["with_passed"], check["with_total"]) +
                         " runs with the Editor, " + pass_count_text(check["baseline_passed"], check["baseline_total"]) + " without.</p>")
            for reason in check["reasons"][:2]:
                parts.append("<blockquote>" + escape(reason) + "</blockquote>")
            parts.append("</div>")
    if not any_failures:
        parts.append("<p>None. Every check passed in every run with the Editor.</p>")

    parts.append("<h2>What the Editor does that Claude doesn&rsquo;t do on its own</h2>"
                 '<p class="muted small">Checks that passed at least half again as often with the Editor.</p><ul>')
    for case in cases:
        for check in case["checks"]:
            if not check["with_total"] or not check["baseline_total"]:
                continue
            with_rate = check["with_passed"] / check["with_total"]
            baseline_rate = check["baseline_passed"] / check["baseline_total"]
            if with_rate - baseline_rate >= 0.5:
                parts.append("<li>" + escape(check["statement"]) + ' <span class="muted small">(' + escape(readable_name(case["name"])) +
                             ": " + percent(with_rate) + " with, " + percent(baseline_rate) + " without)</span></li>")
    parts.append("</ul>")

    style = """
body { font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #1d2a33; max-width: 940px; margin: 40px auto; padding: 0 20px; }
h1 { margin-bottom: 4px; } h2 { margin-top: 40px; border-bottom: 1px solid #dde4e9; padding-bottom: 6px; } h3 { margin-bottom: 6px; }
.muted { color: #5b6b76; } .small { font-size: 14px; }
.explain { background: #f3f6f8; border-radius: 10px; padding: 14px 18px; margin: 18px 0; }
.notice { background: #fff4e5; border-left: 4px solid #e8a33d; padding: 10px 14px; }
.totals { display: flex; gap: 16px; margin: 24px 0; flex-wrap: wrap; } .totals div { flex: 1; min-width: 200px; background: #f3f6f8; border-radius: 10px; padding: 16px; color: #5b6b76; }
.big { display: block; font-size: 34px; font-weight: 700; color: #003049; }
table { width: 100%; border-collapse: collapse; } th, td { text-align: left; padding: 10px 6px; border-bottom: 1px solid #eef2f4; vertical-align: top; }
th { font-size: 13px; color: #5b6b76; font-weight: 600; }
.bar { display: inline-block; width: 80px; height: 8px; background: #eef2f4; border-radius: 4px; vertical-align: middle; margin-right: 8px; }
.fill { height: 8px; border-radius: 4px; } .value { font-variant-numeric: tabular-nums; white-space: nowrap; }
.check { border: 1px solid #dde4e9; border-radius: 8px; padding: 4px 14px; margin: 10px 0; }
blockquote { margin: 8px 0; padding: 6px 12px; background: #f7f9fa; border-left: 3px solid #c6d0d6; font-size: 14px; }
.warn { color: #a0521a; font-size: 13px; }
code { background: #eef2f4; padding: 1px 5px; border-radius: 4px; }
"""
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            "<title>Editor eval results</title><style>" + style + "</style></head><body>" + "\n".join(parts) + "</body></html>\n")


def main():
    arguments = sys.argv[1:]
    output_path = None
    if "--output" in arguments:
        output_index = arguments.index("--output")
        output_path = Path(arguments[output_index + 1])
        arguments = arguments[:output_index] + arguments[output_index + 2:]
    plan = DEFAULT_PLAN
    if "--plan" in arguments:
        plan_index = arguments.index("--plan")
        plan = arguments[plan_index + 1]
        arguments = arguments[:plan_index] + arguments[plan_index + 2:]
    if arguments:
        result_paths = [Path(argument) for argument in arguments]
        runs = load_runs(result_paths[0].parent.parent, result_paths)
        output_path = output_path or result_paths[-1].parent.parent / "eval-summary.html"
    else:
        runs = load_runs()
        output_path = output_path or RESULTS_FOLDER / "eval-summary.html"
    if not runs:
        raise SystemExit("No results yet. Run: python3 tools/run_evals.py")
    output_path.write_text(build_page(runs, plan), encoding="utf-8")
    print("Wrote", output_path)


if __name__ == "__main__":
    main()

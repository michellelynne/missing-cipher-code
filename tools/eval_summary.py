"""Turns eval results into a short, readable HTML page anyone can follow.

Usage: python3 tools/eval_summary.py <aggregate-result.json> [more result files...] [--output page.html]

`claude plugin eval` writes a detailed report for the person debugging a skill. This page is for
everyone else: what each test checks, how much the skill helps, which checks fail, and what
the skill does that the model doesn't do on its own.

Give several result files (for example a full run and a later rerun of the failed cases) and
each case's most recent result is used. Without --output, the page is written as
eval-summary.html next to the last results file.
"""
import html
import json
import re
import statistics
import sys
from pathlib import Path

REPOSITORY_FOLDER = Path(__file__).resolve().parent.parent
EVALS_FOLDER = REPOSITORY_FOLDER / "skills" / "editor" / "evals"
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
    graders = run.get("graders") or []
    evidence = graders[0].get("evidence", "") if graders else ""
    for line_text in evidence.splitlines():
        try:
            yield json.loads(line_text)
        except json.JSONDecodeError:
            continue


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
    if token_count >= 1000000:
        return "{:.1f}M".format(token_count / 1000000)
    return "{:.0f}K".format(token_count / 1000)


def percent(value):
    return "n/a" if value is None else "{:.0%}".format(value)


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


def build_page(result_files):
    cases = [summarize_case(case) for case in latest_cases(result_files)]
    with_scores = [case["with_score"] for case in cases if case["with_score"] is not None]
    baseline_scores = [case["baseline_score"] for case in cases if case["baseline_score"] is not None]
    differences = [case["difference"] for case in cases if case["difference"] is not None]
    models = sorted({model for case in cases for model in case["models"]})
    total_tokens = sum(case["tokens"] for case in cases)
    total_cost = sum(case["cost"] for case in cases)
    run_dates = sorted({result.get("startedAt", "")[:10] for result in result_files if result.get("startedAt")})
    unfinished_total = sum(case["unfinished_runs"] for case in cases)

    parts = ["<h1>Editor eval results</h1>"]
    parts.append('<p class="muted">' + escape(", ".join(run_dates)) + " &middot; " + str(len(cases)) + " test cases &middot; model: " +
                 escape(", ".join(models) or "not recorded") + " &middot; " + tokens_text(total_tokens) +
                 " tokens (${:.2f} at API prices)".format(total_cost) + "</p>")

    parts.append("""<div class="explain"><strong>How to read this page.</strong> Each test case gives the Editor a
realistic request, such as &ldquo;review chapter 3,&rdquo; with sample files that have problems planted on purpose.
Claude does the task once with the Editor skill and once without it, and a second model checks the
result against a list of specific statements, such as &ldquo;asks setup questions before reviewing.&rdquo;
A score is the share of those checks that passed. <em>Adds</em> is the score with the skill minus the
score without it: what the skill contributes beyond what the model already does.</div>""")
    if unfinished_total:
        parts.append('<p class="notice">' + str(unfinished_total) + " run(s) errored or were stopped by the cost limit. "
                     "They are left out of the scores. Rerun them with <code>python3 tools/run_evals.py --rerun --summary</code>.</p>")

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
    if not arguments:
        raise SystemExit(__doc__)
    result_paths = [Path(argument) for argument in arguments]
    result_files = [json.loads(result_path.read_text(encoding="utf-8")) for result_path in result_paths]
    result_files.sort(key=lambda result: result.get("startedAt", ""))
    output_path = output_path or result_paths[-1].with_name("eval-summary.html")
    output_path.write_text(build_page(result_files), encoding="utf-8")
    print("Wrote", output_path)


if __name__ == "__main__":
    main()

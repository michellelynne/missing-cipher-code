"""Turns eval results into a short, readable HTML page.

Usage: python3 tools/eval_summary.py <aggregate-result.json> [output.html]

`claude plugin eval` writes a detailed report. This page answers three questions instead:
how much the skill helps, which checks fail and why, and which checks only pass with the skill.
Without an output path, it writes eval-summary.html next to the results file.
"""
import html
import json
import statistics
import sys
from pathlib import Path

WITH_ARM = "with"


def escape(text):
    return html.escape(str(text))


# Words that should keep their capitals, or read better spelled out, in case and check names.
NAME_WORDS = {"google": "Google", "docs": "Docs", "word": "Word", "scrivener": "Scrivener", "pov": "POV",
              "pass0": "Pass 0", "pass1": "Pass 1", "pass4": "Passes 4 and", "crossref": "cross-reference"}


def readable_name(slug):
    words = slug.split("-")
    if words and words[0].isdigit():
        words = words[1:]
    readable_words = [NAME_WORDS.get(word, word) for word in words]
    sentence = " ".join(readable_words)
    return sentence[0].upper() + sentence[1:] if sentence else sentence


def run_tokens(run):
    """Tokens one run used, read from its session record. Returns 0 when the record has no usage."""
    graders = run.get("graders") or []
    evidence = graders[0].get("evidence", "") if graders else ""
    for line_text in evidence.splitlines():
        try:
            event = json.loads(line_text)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result" and "usage" in event:
            usage = event["usage"]
            return (usage.get("input_tokens", 0) + usage.get("output_tokens", 0) +
                    usage.get("cache_read_input_tokens", 0) + usage.get("cache_creation_input_tokens", 0))
    return 0


def tokens_text(token_count):
    if token_count >= 1000000:
        return "{:.1f}M".format(token_count / 1000000)
    return "{:.0f}K".format(token_count / 1000)


def completed(runs):
    return [run for run in runs if not run.get("error")]


def mean_score(runs):
    finished_runs = completed(runs)
    if not finished_runs:
        return None
    return statistics.mean(run["score"] for run in finished_runs)


def percent(value):
    return "n/a" if value is None else "{:.0%}".format(value)


def baseline_arm_name(arms):
    other_names = [arm_name for arm_name in arms if arm_name != WITH_ARM]
    return other_names[0] if other_names else None


def grader_results(runs, grader_name):
    results = []
    for run in completed(runs):
        for grader in run.get("graders", []):
            if grader["name"] == grader_name and grader.get("scored", True):
                results.append(grader)
    return results


def summarize_case(case):
    arms = case["arms"]
    baseline_name = baseline_arm_name(arms)
    with_runs = arms.get(WITH_ARM, [])
    baseline_runs = arms.get(baseline_name, []) if baseline_name else []
    with_score = mean_score(with_runs)
    baseline_score = mean_score(baseline_runs)
    checks = []
    for grader in case["graders"]:
        with_results = grader_results(with_runs, grader["name"])
        baseline_results = grader_results(baseline_runs, grader["name"])
        checks.append({
            "name": grader["name"],
            "statement": grader.get("graderMarkdown") or grader.get("config", {}).get("criteria", ""),
            "with_passed": sum(1 for result in with_results if result["passed"]),
            "with_total": len(with_results),
            "baseline_passed": sum(1 for result in baseline_results if result["passed"]),
            "baseline_total": len(baseline_results),
            "failure_reasons": [result.get("explanation", "") for result in with_results if not result["passed"]],
        })
    all_runs = with_runs + baseline_runs
    return {
        "name": case["name"],
        "with_score": with_score,
        "baseline_score": baseline_score,
        "difference": None if with_score is None or baseline_score is None else with_score - baseline_score,
        "runs": len(all_runs),
        "errored_runs": sum(1 for run in all_runs if run.get("error")),
        "cost": sum(run.get("costUsd", 0) for run in all_runs),
        "tokens": sum(run_tokens(run) for run in all_runs),
        "checks": checks,
    }


def score_bar(score, color):
    if score is None:
        return '<span class="muted">not run</span>'
    width = round(score * 100)
    return ('<div class="bar"><div class="fill" style="width:' + str(width) + '%;background:' + color + '"></div></div>'
            '<span class="value">' + percent(score) + "</span>")


def build_page(result):
    cases = [summarize_case(case) for case in result["cases"]]
    with_scores = [case["with_score"] for case in cases if case["with_score"] is not None]
    baseline_scores = [case["baseline_score"] for case in cases if case["baseline_score"] is not None]
    differences = [case["difference"] for case in cases if case["difference"] is not None]

    notices = []
    if result.get("partial"):
        notices.append("This run stopped early (" + escape(result.get("partialReason", "unknown reason")).replace("_", " ") +
                       "), so some cases have fewer runs or none.")
    errored_total = sum(case["errored_runs"] for case in cases)
    if errored_total:
        notices.append(str(errored_total) + " run(s) errored or hit the cost limit. They are left out of the scores below.")

    parts = []
    parts.append("<h1>Eval results</h1>")
    parts.append('<p class="muted">' + escape(result.get("startedAt", "")[:10]) + " &middot; Claude Code " +
                 escape(result.get("claudeVersion", "")) + " &middot; " +
                 "{:.0f} minutes".format(result.get("durationSeconds", 0) / 60) + " &middot; " +
                 tokens_text(sum(case["tokens"] for case in cases)) + " tokens (${:.2f} at API prices)".format(result.get("costUsd", 0)) + "</p>")
    for notice in notices:
        parts.append('<p class="notice">' + notice + "</p>")

    parts.append('<div class="totals">')
    parts.append('<div><span class="big">' + percent(statistics.mean(with_scores) if with_scores else None) + "</span>with the skill</div>")
    parts.append('<div><span class="big">' + percent(statistics.mean(baseline_scores) if baseline_scores else None) + "</span>without it</div>")
    average_difference = statistics.mean(differences) if differences else None
    parts.append('<div><span class="big">' + ("n/a" if average_difference is None else "{:+.0f}".format(average_difference * 100)) +
                 "</span>points the skill adds</div>")
    parts.append("</div>")

    parts.append("<h2>By case</h2><table><tr><th>Case</th><th>With the skill</th><th>Without</th><th>Adds</th><th>Runs</th><th>Tokens</th><th>At API prices</th></tr>")
    for case in cases:
        difference_text = "n/a" if case["difference"] is None else "{:+.0f}".format(case["difference"] * 100)
        parts.append("<tr><td>" + escape(readable_name(case["name"])) + "</td><td>" + score_bar(case["with_score"], "#177E89") +
                     "</td><td>" + score_bar(case["baseline_score"], "#9aa5ad") + "</td><td>" + difference_text +
                     "</td><td>" + str(case["runs"]) + "</td><td>" + tokens_text(case["tokens"]) + "</td><td>${:.2f}</td></tr>".format(case["cost"]))
    parts.append("</table>")

    parts.append("<h2>Checks that failed with the skill</h2>")
    any_failures = False
    for case in cases:
        failing_checks = [check for check in case["checks"] if check["with_total"] and check["with_passed"] < check["with_total"]]
        if not failing_checks:
            continue
        any_failures = True
        parts.append("<h3>" + escape(readable_name(case["name"])) + "</h3>")
        for check in failing_checks:
            parts.append('<div class="check"><p><strong>' + escape(check["statement"]) + "</strong></p>")
            parts.append('<p class="muted">Passed ' + str(check["with_passed"]) + " of " + str(check["with_total"]) +
                         " runs with the skill, " + str(check["baseline_passed"]) + " of " + str(check["baseline_total"]) + " without.</p>")
            for reason in check["failure_reasons"][:2]:
                parts.append("<blockquote>" + escape(reason) + "</blockquote>")
            parts.append("</div>")
    if not any_failures:
        parts.append("<p>None.</p>")

    parts.append("<h2>What only passes with the skill</h2><ul>")
    for case in cases:
        for check in case["checks"]:
            if not check["with_total"] or not check["baseline_total"]:
                continue
            with_rate = check["with_passed"] / check["with_total"]
            baseline_rate = check["baseline_passed"] / check["baseline_total"]
            if with_rate - baseline_rate >= 0.5:
                parts.append("<li>" + escape(check["statement"]) + ' <span class="muted">(' + escape(readable_name(case["name"])) +
                             ": " + percent(with_rate) + " with, " + percent(baseline_rate) + " without)</span></li>")
    parts.append("</ul>")

    style = """
body { font: 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #1d2a33; max-width: 920px; margin: 40px auto; padding: 0 20px; }
h1 { margin-bottom: 4px; } h2 { margin-top: 40px; border-bottom: 1px solid #dde4e9; padding-bottom: 6px; } h3 { margin-bottom: 6px; }
.muted { color: #5b6b76; font-size: 14px; }
.notice { background: #fff4e5; border-left: 4px solid #e8a33d; padding: 10px 14px; }
.totals { display: flex; gap: 16px; margin: 24px 0; } .totals div { flex: 1; background: #f3f6f8; border-radius: 10px; padding: 16px; color: #5b6b76; }
.big { display: block; font-size: 34px; font-weight: 700; color: #003049; }
table { width: 100%; border-collapse: collapse; } th, td { text-align: left; padding: 8px 6px; border-bottom: 1px solid #eef2f4; vertical-align: middle; }
th { font-size: 13px; color: #5b6b76; font-weight: 600; }
.bar { display: inline-block; width: 90px; height: 8px; background: #eef2f4; border-radius: 4px; vertical-align: middle; margin-right: 8px; }
.fill { height: 8px; border-radius: 4px; } .value { font-variant-numeric: tabular-nums; }
.check { border: 1px solid #dde4e9; border-radius: 8px; padding: 6px 14px; margin: 10px 0; }
blockquote { margin: 8px 0; padding: 6px 12px; background: #f7f9fa; border-left: 3px solid #c6d0d6; font-size: 14px; }
"""
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            "<title>Eval results</title><style>" + style + "</style></head><body>" + "\n".join(parts) + "</body></html>\n")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    result_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else result_path.with_name("eval-summary.html")
    output_path.write_text(build_page(json.loads(result_path.read_text(encoding="utf-8"))), encoding="utf-8")
    print("Wrote", output_path)


if __name__ == "__main__":
    main()

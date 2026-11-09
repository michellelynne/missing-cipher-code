#!/usr/bin/env bash
# Measures how much of a Claude subscription a command uses, such as an eval run.
#
# Usage, from the top of the repository:
#   tools/measure_plan_usage.sh "short label" claude plugin eval skills/editor --runs 1 --model sonnet ...
#
# It opens Claude Code, types /usage, and saves the session and weekly percentages; runs the
# command; waits a minute for usage to catch up; reads /usage again; and adds a line to
# plan-usage.csv in the eval results folder. Opening Claude Code to read /usage sends nothing
# to Claude.
#
# For subscription plans (Pro, Max). With an API key, /usage shows no plan bars; use the dollar
# figures the eval reports instead. Needs `expect`, which comes with macOS.
#
# Limits: it reads the /usage screen, so a change to that screen can break it (the numbers come
# back empty). Anything else you do in Claude while it runs, chat included, counts too.

set -euo pipefail

if [ "$#" -lt 2 ]; then
  sed -n '2,17p' "$0"
  exit 1
fi

run_label="$1"
shift

repository_folder="$(cd "$(dirname "$0")/.." && pwd)"
results_folder="$repository_folder/skills/editor/evals/results"
log_path="$results_folder/plan-usage.csv"
wait_seconds="${PLAN_USAGE_WAIT_SECONDS:-60}"
mkdir -p "$results_folder"

for required_program in expect claude python3; do
  if ! command -v "$required_program" > /dev/null 2>&1; then
    echo "Needs $required_program, which isn't installed." >&2
    exit 1
  fi
done

# Opens Claude Code in the repository, types /usage, and saves the screen to the given file.
capture_usage_screen() {
  local capture_path="$1"
  # Waits a fixed time at each step: the screen is drawn with terminal codes between the words,
  # so watching for particular text isn't reliable. Takes about 25 seconds.
  REPOSITORY_FOLDER="$repository_folder" CAPTURE_PATH="$capture_path" expect <<'EXPECT_SCRIPT' > /dev/null
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
EXPECT_SCRIPT
}

read_usage() {
  local capture_path
  capture_path="$(mktemp)"
  capture_usage_screen "$capture_path" || true
  python3 "$repository_folder/tools/plan_usage.py" "$capture_path"
  rm -f "$capture_path"
}

json_field() {
  python3 -c 'import json, sys; value = json.loads(sys.argv[1]).get(sys.argv[2]); print("" if value is None else value)' "$1" "$2"
}

echo "Reading plan usage before the run..."
usage_before="$(read_usage)"
session_before="$(json_field "$usage_before" session_percent)"
week_before="$(json_field "$usage_before" week_percent)"
echo "  Before: session ${session_before:-?}%, week ${week_before:-?}%"
problem_before="$(json_field "$usage_before" problem)"
if [ -n "$problem_before" ]; then
  echo "  $problem_before" >&2
  exit 1
fi
if [ -z "$week_before" ]; then
  echo "  Couldn't read the weekly number. The /usage screen may have changed; the run will still go ahead." >&2
fi

start_seconds="$(date +%s)"
set +e
"$@"
command_status=$?
set -e
run_minutes=$(( ($(date +%s) - start_seconds + 30) / 60 ))

echo "Waiting ${wait_seconds} seconds for usage to update..."
sleep "$wait_seconds"
usage_after="$(read_usage)"
session_after="$(json_field "$usage_after" session_percent)"
week_after="$(json_field "$usage_after" week_percent)"

week_change=""
if [ -n "$week_before" ] && [ -n "$week_after" ]; then
  week_change=$(( week_after - week_before ))
fi
session_note=""
if [ -n "$session_before" ] && [ -n "$session_after" ] && [ "$session_after" -lt "$session_before" ]; then
  session_note="session window reset during the run"
fi

if [ ! -f "$log_path" ]; then
  echo "date,label,minutes,session_before,session_after,week_before,week_after,week_change,exit_status,note,command" > "$log_path"
fi
csv_command="$(printf '%s ' "$@" | sed 's/"/""/g; s/ $//')"
csv_label="$(printf '%s' "$run_label" | sed 's/"/""/g')"
echo "$(date '+%Y-%m-%d %H:%M'),\"$csv_label\",$run_minutes,$session_before,$session_after,$week_before,$week_after,$week_change,$command_status,$session_note,\"$csv_command\"" >> "$log_path"

echo
echo "Plan usage for \"$run_label\" ($run_minutes minutes):"
echo "  Session: ${session_before:-?}% -> ${session_after:-?}% ${session_note:+($session_note)}"
echo "  Week:    ${week_before:-?}% -> ${week_after:-?}%${week_change:+ (+$week_change points)}"
echo "  Saved to ${log_path#"$repository_folder"/}"
exit "$command_status"

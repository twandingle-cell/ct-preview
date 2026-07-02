#!/usr/bin/env bash
set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

CODEX_ASK="$HOME/.claude/bin/codex-ask.sh"
if [ ! -x "$CODEX_ASK" ]; then
    CODEX_ASK="./scripts/codex-ask.sh"
fi

for cmd in claude python3; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Missing required command: $cmd" >&2
        exit 1
    fi
done

# The claude -p calls below are pure text generation, they must never touch
# the filesystem, the network, or run a command. Without this, a nested
# Claude instance keeps its normal tool access and can decide to act like an
# agent instead of a text pipe, for example it might notice an old report
# already exists and summarize that instead of generating a fresh one, or
# in the worst case invoke deliver.py itself next to a live API key. This
# denylist is what turns claude -p into the same kind of sandboxed, read-only
# text pipe that codex-ask.sh already gives us for Codex.
CLAUDE_NO_TOOLS="Agent,Artifact,AskUserQuestion,Bash,Edit,Glob,Grep,NotebookEdit,Read,ScheduleWakeup,SendUserFile,ShowOnboardingRolePicker,Skill,ToolSearch,Workflow,Write,WebFetch,WebSearch,TaskCreate,TaskGet,TaskList,TaskOutput,TaskStop,TaskUpdate,CronCreate,CronDelete,CronList,EnterPlanMode,EnterWorktree,ExitPlanMode,ExitWorktree,DesignSync,PushNotification,SendMessage,ReportFindings"

echo "==> Step 1: scanning premarket data"
source .venv/bin/activate
python3 scan.py
if [ ! -s packet.json ]; then
    echo "scan.py produced no packet.json, aborting" >&2
    exit 1
fi

echo "==> Step 2: Claude analyst pass (this can take a couple of minutes)"
{ cat prompt_claude.md; echo; echo "=== INPUT: packet.json ==="; cat packet.json; } \
    | claude -p --disallowedTools "$CLAUDE_NO_TOOLS" > claude_view.md
if [ ! -s claude_view.md ]; then
    echo "Claude analyst pass produced no output, aborting" >&2
    exit 1
fi

echo "==> Step 3: Codex analyst pass (independent, blind)"
if [ -x "$CODEX_ASK" ] && { cat prompt_codex.md; echo; echo "=== INPUT: packet.json ==="; cat packet.json; } | "$CODEX_ASK" > codex_view.md; then
    echo "    Codex pass succeeded"
else
    echo "    Codex pass failed or codex-ask.sh not found, recording as unavailable" >&2
    cat > codex_view.md <<'EOF'
# Codex View — Independent Second Opinion

STATUS: UNAVAILABLE. codex-ask.sh returned a nonzero exit code, or was not
found, on this run. Check that codex is installed (npm install -g
@openai/codex or brew install codex), logged in (codex login), and that
this machine has network access to api.openai.com.
EOF
fi

echo "==> Step 4: merge pass (this can take a couple of minutes)"
{
    cat prompt_merge.md
    echo
    echo "=== INPUT: packet.json ==="
    cat packet.json
    echo
    echo "=== INPUT: claude_view.md ==="
    cat claude_view.md
    echo
    echo "=== INPUT: codex_view.md ==="
    cat codex_view.md
} | claude -p --disallowedTools "$CLAUDE_NO_TOOLS" > REPORT.md
if [ ! -s REPORT.md ]; then
    echo "Merge pass produced no output, aborting" >&2
    exit 1
fi

echo "==> Step 5: render HTML"
RENDER_OUTPUT="$(python3 render_html.py REPORT.md)"
echo "$RENDER_OUTPUT"
HTML_PATH="$(echo "$RENDER_OUTPUT" | sed -n 's/^Wrote //p')"
if [ -z "$HTML_PATH" ] || [ ! -s "$HTML_PATH" ]; then
    echo "render_html.py did not produce an HTML file, aborting" >&2
    exit 1
fi

echo "==> Step 6: deliver"
python3 deliver.py "$HTML_PATH"

echo "==> Done. Report: REPORT.md, HTML: $HTML_PATH"

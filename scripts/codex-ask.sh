#!/usr/bin/env bash
set -uo pipefail

if [ "$#" -ge 1 ]; then
    PROMPT="$1"
else
    PROMPT="$(cat)"
fi

OUTPUT_FILE="$(mktemp)"
LOG_FILE="$(mktemp)"
trap 'rm -f "$OUTPUT_FILE" "$LOG_FILE"' EXIT

codex exec --skip-git-repo-check -s read-only -o "$OUTPUT_FILE" "$PROMPT" < /dev/null > "$LOG_FILE" 2>&1

if [ -s "$OUTPUT_FILE" ]; then
    cat "$OUTPUT_FILE"
else
    cat "$LOG_FILE" >&2
    exit 1
fi

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

stop_tree() {
  local pid="$1"
  local child
  if ! kill -0 "$pid" 2>/dev/null; then return 0; fi
  while read -r child; do
    [ -n "$child" ] && stop_tree "$child"
  done < <(pgrep -P "$pid" 2>/dev/null || true)
  kill -TERM "$pid" 2>/dev/null || true
}

for name in frontend backend ollama; do
  f="$ROOT/logs/$name.pid"
  if [ -f "$f" ]; then
    pid="$(cat "$f" 2>/dev/null || true)"
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then stop_tree "$pid"; fi
    rm -f "$f"
  fi
done
echo "Stop signals sent to AGRO AI processes started by scripts/start_all.sh."

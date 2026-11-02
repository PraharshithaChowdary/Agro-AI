#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/logs"
if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama is not installed. In Codespaces run: curl -fsSL https://ollama.com/install.sh | sh" >&2
  exit 1
fi
if curl -fsS http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
  echo "Ollama is already running."
  exit 0
fi
nohup ollama serve > "$ROOT/logs/ollama.log" 2>&1 < /dev/null &
echo $! > "$ROOT/logs/ollama.pid"
for i in $(seq 1 40); do
  if curl -fsS http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
    echo "Ollama server is ready."
    exit 0
  fi
  sleep 1
done
echo "Ollama did not start. Inspect logs/ollama.log" >&2
exit 1

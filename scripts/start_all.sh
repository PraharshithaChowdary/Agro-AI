#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [ -f .env ]; then set -a; . ./.env; set +a; fi
mkdir -p logs backend/uploads

if [ ! -x .venv/bin/python ]; then
  echo "Python environment is missing. Run: bash .devcontainer/post-create.sh" >&2
  exit 1
fi
if [ ! -x frontend/node_modules/.bin/vite ]; then
  echo "Frontend dependencies are missing. Run: cd frontend && npm ci" >&2
  exit 1
fi

source .venv/bin/activate
bash scripts/start_ollama.sh

MODEL_LIST="$(ollama list 2>/dev/null || true)"
VISION_MODEL="${OLLAMA_VISION_MODEL:-qwen2.5vl:3b}"
CHAT_MODEL="${OLLAMA_CHAT_MODEL:-qwen2.5:1.5b}"
if ! printf '%s\n' "$MODEL_LIST" | awk 'NR > 1 {print $1}' | grep -Fq "$VISION_MODEL"; then
  echo "NOTICE: the configured image-analysis model is not installed. Run: bash scripts/pull_models.sh"
fi
if ! printf '%s\n' "$MODEL_LIST" | awk 'NR > 1 {print $1}' | grep -Fq "$CHAT_MODEL"; then
  echo "NOTICE: the configured chat model is not installed. Run: bash scripts/pull_models.sh"
fi

if curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
  echo "Backend is already healthy on port 8000; leaving it running."
else
  nohup .venv/bin/uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 < /dev/null &
  echo $! > logs/backend.pid
  echo "Waiting for backend startup..."
  READY=0
  for _ in $(seq 1 60); do
    if curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then READY=1; break; fi
    sleep 1
  done
  if [ "$READY" -ne 1 ]; then
    echo "Backend failed to become healthy. Last backend log lines:" >&2
    tail -n 60 logs/backend.log >&2 || true
    exit 1
  fi
fi

if curl -fsS http://127.0.0.1:5173 >/dev/null 2>&1; then
  echo "Frontend is already responding on port 5173; leaving it running."
else
  (cd frontend && nohup npm run dev -- --host 0.0.0.0 > "$ROOT/logs/frontend.log" 2>&1 < /dev/null & echo $! > "$ROOT/logs/frontend.pid")
  echo "Waiting for frontend startup..."
  READY=0
  for _ in $(seq 1 40); do
    if curl -fsS http://127.0.0.1:5173 >/dev/null 2>&1; then READY=1; break; fi
    sleep 1
  done
  if [ "$READY" -ne 1 ]; then
    echo "Frontend failed to become ready. Last frontend log lines:" >&2
    tail -n 60 logs/frontend.log >&2 || true
    exit 1
  fi
fi

printf '\nAGRO AI is responding.\n'
echo "Open forwarded port 5173 (AGRO AI Web)."
echo "Backend API docs: forwarded port 8000, path /docs."
echo "Logs: logs/backend.log, logs/frontend.log, logs/ollama.log"
echo "If analysis reports a missing model, run: bash scripts/pull_models.sh"

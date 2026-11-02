#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [ -f .env ]; then set -a; . ./.env; set +a; fi
if ! command -v ollama >/dev/null 2>&1; then
  echo "Ollama is not installed. In Codespaces run: curl -fsSL https://ollama.com/install.sh | sh" >&2
  exit 1
fi
bash scripts/start_ollama.sh
VISION_MODEL="${OLLAMA_VISION_MODEL:-qwen2.5vl:3b}"
CHAT_MODEL="${OLLAMA_CHAT_MODEL:-qwen2.5:1.5b}"
echo "Downloading vision model: ${VISION_MODEL}"
echo "This is a multi-GB download and needs internet access plus free disk space."
ollama pull "$VISION_MODEL"
echo "Downloading chat model: ${CHAT_MODEL}"
ollama pull "$CHAT_MODEL"
echo
echo "Installed models:"
ollama list
printf '\nModel downloads finished. Next run: bash scripts/start_all.sh\n'

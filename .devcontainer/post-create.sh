#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt

if [ -f frontend/package-lock.json ]; then
  (cd frontend && npm ci)
else
  (cd frontend && npm install)
fi

if [ ! -f .env ]; then
  cp .env.example .env
  SECRET="$(python - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)"
  python - "$SECRET" <<'PY'
from pathlib import Path
import sys
p=Path('.env')
s=p.read_text()
s=s.replace('JWT_SECRET_KEY=replace-this-with-a-random-secret', 'JWT_SECRET_KEY='+sys.argv[1])
p.write_text(s)
PY
fi

# Ollama is installed on first setup if the official installer is reachable.
# It is intentionally not started or model-pulled during postCreate to keep startup manageable.
if ! command -v ollama >/dev/null 2>&1; then
  echo "Installing Ollama..."
  if curl -fsSL https://ollama.com/install.sh -o /tmp/ollama-install.sh; then
    if ! sh /tmp/ollama-install.sh; then
      echo "WARNING: Ollama installation did not complete. Retry in the Codespaces terminal with: curl -fsSL https://ollama.com/install.sh | sh"
    fi
  else
    echo "WARNING: Could not download the Ollama installer during setup. Retry in the Codespaces terminal with: curl -fsSL https://ollama.com/install.sh | sh"
  fi
fi

mkdir -p logs backend/uploads
touch backend/uploads/.gitkeep
python backend/scripts/bootstrap_database.py
echo
echo "AGRO AI dependencies are installed."
echo "Next: bash scripts/pull_models.sh, then bash scripts/start_all.sh"

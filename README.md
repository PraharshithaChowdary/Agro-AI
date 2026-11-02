# AGRO AI — Full-stack Student Project (Windows + Ollama)

**Smart Agriculture. Healthy Lives. Better Future.**

AGRO AI is a full-stack React + TypeScript + FastAPI application with the existing student-project interfaces: dashboard, sign-in/sign-up, Indian Plant Explorer, Analyse My Plant, Crop Analysis, Soil Analysis, Better Nutrition, Weekly Diet Plan and Agricultural Assistant. SQLite stores accounts and user-scoped histories.

The local AI integration uses **Ollama + Qwen2.5-VL 3B for image understanding** and **Qwen2.5 1.5B for agricultural chat**. It requires no paid inference API key. Image reports are structured visual screening, not guaranteed diagnoses.

> **Accuracy note:** No general-purpose vision model can promise perfect recognition of every species or disease. The report distinguishes directly visible observations from possible causes, avoids fabricated confidence percentages, and does not claim internal fruit rot, food safety, measured soil pH/NPK or confirmed plant disease. To claim real accuracy, evaluate on labelled held-out images from the crops and conditions you target.

## Quick start — Windows 10/11

### 1. Install the prerequisites once

- **Ollama for Windows:** [Official installer](https://ollama.com/download/windows). Ollama runs as a local background app and serves its API at `http://localhost:11434` on the same computer. See the [official Windows documentation](https://ollama.readthedocs.io/en/windows/).
- **Node.js LTS:** [nodejs.org](https://nodejs.org/) (npm is included).
- **Python 3.12+** recommended: [python.org](https://www.python.org/downloads/windows/). Enable the option to add Python to PATH during installation if available.
- Keep a few GB of free disk space for the two local models; the vision model download is multi-GB.

After installing, reopen VS Code/Command Prompt so PATH updates are visible. You do not normally need Administrator privileges to install the Ollama Windows desktop app.

### 2. Extract and set up the project

Extract this ZIP to a normal writable folder, for example `C:\AGRO_AI`. Avoid running it from inside the ZIP or from a protected Windows folder.

Double-click **`setup_windows.bat`**. It creates `.venv`, installs backend and frontend dependencies, copies `.env.example` to `.env`, creates a unique local JWT secret, and creates log/upload folders. Initial installation requires internet.

### 3. Download the Ollama models (one time)

Double-click **`download_models.bat`**, or run these commands in a terminal once Ollama is running:

```cmd
ollama pull qwen2.5vl:3b
ollama pull qwen2.5:1.5b
```

The official Qwen2.5-VL model listing includes a 3B vision tag. If Ollama reports that the model is unsupported, update Ollama using its latest official Windows installer, then retry. See the [Ollama Qwen2.5-VL model page](https://registry.ollama.com/library/qwen2.5vl).

### 4. Launch AGRO AI

Double-click **`start_agro_ai.bat`**. It opens separate backend and frontend terminal windows and opens the app at:

- Web app: `http://localhost:5173`
- Backend health: `http://127.0.0.1:8000/api/health`
- API docs: `http://127.0.0.1:8000/docs`
- Ollama readiness: `http://127.0.0.1:8000/api/ollama/status`

Keep the backend and frontend terminal windows open while you use the app. To stop a service, press **Ctrl+C** in that service's terminal window. Do not run duplicate launchers if ports 8000/5173 are already occupied.

### 5. Verify setup

Double-click **`diagnose_agro_ai.bat`** to print RAM, Python, Node, Ollama version, installed models and app endpoint checks. Or use:

```cmd
ollama list
curl http://127.0.0.1:8000/api/ollama/status
```

For a reliable first image test, use a clear, well-lit image with one leaf/fruit filling most of the frame. The first request may be slower because the model must load into RAM.

## Hardware notes for a 16 GB laptop

The default image model is Qwen2.5-VL 3B. A laptop with 16 GB RAM is recommended; available memory varies with browsers and other applications. The project defaults resize images to a 256 px longest edge, use a 2048-token context, limit vision output to 160 tokens, keep models warm for 10 minutes, and serialize local inference requests to reduce memory spikes. The compact image setting is chosen for faster local screening. If the model runner still crashes, close memory-heavy apps and inspect Ollama's server log; upgrading RAM is not the first troubleshooting step.

Default `.env` settings include:

```dotenv
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_CHAT_MODEL=qwen2.5:1.5b
OLLAMA_VISION_MODEL=qwen2.5vl:3b
OLLAMA_TIMEOUT_SECONDS=360
OLLAMA_KEEP_ALIVE=10m
OLLAMA_NUM_CTX=2048
OLLAMA_IMAGE_MAX_SIDE=256
OLLAMA_IMAGE_JPEG_QUALITY=60
OLLAMA_VISION_NUM_PREDICT=160
```

Change settings in the root `.env` and restart the backend. Keep `.env` private; never commit access tokens or a real user's database.

## Troubleshooting (Windows)

- **`ollama` command not found:** install the official Windows app, fully finish installation, then open a new terminal.
- **Ollama not reachable:** open Ollama from the Start menu and confirm `http://127.0.0.1:11434/api/version` responds; alternatively run `ollama serve` in a terminal if the desktop server is not already running.
- **Model missing:** rerun `download_models.bat`.
- **`unexpected EOF`, `runner process has terminated`, HTTP 500/502:** this means the model runner failed, not that the frontend cannot load. Update Ollama from the official installer, close heavy applications, retry a smaller clear image, and inspect `%LOCALAPPDATA%\Ollama\server.log`. If it repeats, run `diagnose_agro_ai.bat` and share its output.
- **Port 8000 or 5173 already in use:** check whether AGRO AI is already running in another terminal window. Stop that copy with Ctrl+C before restarting. Do not force-kill unrelated processes.
- **Frontend says request failed:** open backend health and `/api/ollama/status` links above and inspect the backend terminal traceback.
- **Plant catalogue is empty:** backend startup should import the bundled catalogue into the new SQLite database on first run; inspect the backend window for any bootstrap error.

## GitHub Codespaces (optional)

The project keeps the `.devcontainer` configuration and Linux scripts for Codespaces. In the Codespaces terminal, run `bash scripts/pull_models.sh` once and then `bash scripts/start_all.sh`. Note that Codespaces RAM/CPU differs from your laptop and a CPU-only machine can be slower or more constrained.

## Stack and tests

- Frontend: React 18, TypeScript, Vite, Tailwind CSS, React Router, Axios.
- Backend: FastAPI, SQLAlchemy, Pydantic and SQLite.
- Local AI: Ollama native `/api/chat` endpoint with image payloads.
- Catalogue: bundled plant manifest, imported into a fresh local database.
- Test contracts with `pytest backend/tests` from a Python environment where backend requirements are installed. These tests validate report normalization and API contracts without claiming live model accuracy. Live accuracy needs a labelled, held-out evaluation set.

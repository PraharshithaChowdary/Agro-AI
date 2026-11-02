@echo off
cd /d "%~dp0"
title AGRO AI Backend - FastAPI
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Python environment is missing. Run setup_windows.bat first.
  pause
  exit /b 1
)
set "PYTHONPATH=%~dp0backend"
"%~dp0.venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir "%~dp0backend" --host 0.0.0.0 --port 8000 --reload
if errorlevel 1 echo Backend stopped with an error. Read the traceback above.
pause

@echo off
setlocal
cd /d "%~dp0"
title AGRO AI - Windows Setup

echo ================================================================
echo  AGRO AI - Windows local setup
echo ================================================================
echo.
where node >nul 2>nul
if errorlevel 1 (
  echo ERROR: Node.js was not found. Install Node.js LTS from https://nodejs.org/ and reopen this window.
  pause
  exit /b 1
)
where npm.cmd >nul 2>nul
if errorlevel 1 (
  echo ERROR: npm was not found. Repair your Node.js installation.
  pause
  exit /b 1
)
where ollama >nul 2>nul
if errorlevel 1 (
  echo ERROR: Ollama was not found.
  echo Install Ollama for Windows from https://ollama.com/download/windows
  echo Then reopen this window and run setup_windows.bat again.
  pause
  exit /b 1
)
set "PYLAUNCH=python"
where py >nul 2>nul
if not errorlevel 1 set "PYLAUNCH=py -3"
%PYLAUNCH% --version
if errorlevel 1 (
  echo ERROR: Python 3 was not found. Install Python 3.12 or newer from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo Creating Python virtual environment...
  %PYLAUNCH% -m venv .venv
  if errorlevel 1 goto :fail
)
echo Installing/updating Python dependencies. This can take several minutes...
"%~dp0.venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :fail
"%~dp0.venv\Scripts\python.exe" -m pip install -r backend\requirements.txt
if errorlevel 1 goto :fail
if not exist "frontend\node_modules\vite\bin\vite.js" (
  echo Installing frontend dependencies with npm ci...
  pushd frontend
  call npm.cmd ci
  if errorlevel 1 (popd & goto :fail)
  popd
) else (
  echo Frontend dependencies already appear to be installed.
)
if not exist ".env" (
  copy ".env.example" ".env" >nul
  if errorlevel 1 goto :fail
  "%~dp0.venv\Scripts\python.exe" -c "import secrets,pathlib; p=pathlib.Path('.env'); s=p.read_text(encoding='utf-8'); s=s.replace('JWT_SECRET_KEY=replace-this-with-a-random-secret','JWT_SECRET_KEY='+secrets.token_urlsafe(48)); p.write_text(s,encoding='utf-8')"
  if errorlevel 1 goto :fail
  echo Created .env with a unique local JWT secret.
) else (
  echo Existing .env preserved.
)
if not exist "logs" mkdir logs
if not exist "backend\uploads" mkdir backend\uploads

echo.
echo Setup complete. Next run download_models.bat once, then start_agro_ai.bat.
echo Keep your .env file private and never commit it to GitHub.
pause
exit /b 0
:fail
echo.
echo Setup failed. Read the error above, fix that issue, then rerun setup_windows.bat.
pause
exit /b 1

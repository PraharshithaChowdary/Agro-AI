@echo off
setlocal
cd /d "%~dp0"
title AGRO AI - Local Diagnostics

echo ================================================================
echo  AGRO AI - Windows Diagnostics
echo ================================================================
echo.
echo [System memory]
powershell -NoProfile -Command "$os=Get-CimInstance Win32_OperatingSystem; 'Total RAM: {0:N2} GB' -f ($os.TotalVisibleMemorySize/1MB); 'Free RAM now: {0:N2} GB' -f ($os.FreePhysicalMemory/1MB)"
echo.
echo [Python]
if exist ".venv\Scripts\python.exe" (".venv\Scripts\python.exe" --version) else (echo .venv is missing)
echo.
echo [Node and npm]
node --version 2>nul
call npm.cmd --version 2>nul
echo.
echo [Ollama version and API]
ollama --version 2>nul
curl.exe -s http://127.0.0.1:11434/api/version
echo.
echo [Installed Ollama models]
ollama list 2>nul
echo.
echo [Frontend endpoint]
curl.exe -I --max-time 5 http://127.0.0.1:5173 2>nul
echo.
echo [Backend health endpoint]
curl.exe -s --max-time 5 http://127.0.0.1:8000/api/health
echo.
echo [AGRO AI Ollama readiness]
curl.exe -s --max-time 5 http://127.0.0.1:8000/api/ollama/status
echo.
echo If image analysis fails, inspect the Ollama server log at %%LOCALAPPDATA%%\Ollama\server.log and check free RAM.
pause

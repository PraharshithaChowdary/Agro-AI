@echo off
setlocal
cd /d "%~dp0"
title AGRO AI - Download Ollama Models
where ollama >nul 2>nul
if errorlevel 1 (
  echo ERROR: Ollama is not installed. Install from https://ollama.com/download/windows
  pause
  exit /b 1
)
curl.exe -fsS http://127.0.0.1:11434/api/version >nul 2>nul
if errorlevel 1 (
  echo Ollama API is not responding. Starting a local Ollama server window...
  start "AGRO AI - Ollama Server" cmd.exe /k "ollama serve"
  timeout /t 5 /nobreak >nul
  curl.exe -fsS http://127.0.0.1:11434/api/version >nul 2>nul
  if errorlevel 1 (
    echo ERROR: Ollama API did not start. Open the Ollama app from the Windows Start menu and retry.
    pause
    exit /b 1
  )
)
echo.
echo Downloading Qwen2.5-VL 3B for image screening. This is several GB.
echo.
ollama pull qwen2.5vl:3b
if errorlevel 1 goto :fail
echo.
echo Downloading Qwen2.5 1.5B for agriculture chat.
echo.
ollama pull qwen2.5:1.5b
if errorlevel 1 goto :fail
echo.
echo Model list:
ollama list
echo.
echo Model downloads complete. Run start_agro_ai.bat to launch AGRO AI.
pause
exit /b 0
:fail
echo.
echo Model download failed. Check internet connection and free disk space, then rerun this script.
pause
exit /b 1

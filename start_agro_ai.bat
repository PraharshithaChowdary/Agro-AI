@echo off
setlocal
cd /d "%~dp0"
title AGRO AI - Local Launcher

echo ================================================================
echo  AGRO AI - Local Windows Launcher
echo ================================================================
echo.
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Python environment is missing. Run setup_windows.bat first.
  goto :fail
)
if not exist "frontend\node_modules\vite\bin\vite.js" (
  echo ERROR: Frontend dependencies are missing. Run setup_windows.bat first.
  goto :fail
)
where curl.exe >nul 2>nul
if errorlevel 1 (
  echo ERROR: curl.exe was not found. Install/repair Windows curl and retry.
  goto :fail
)

rem Use the Vite proxy so the web app always calls this project's port 8000 API.
>"frontend\.env.local" echo VITE_API_BASE_URL=/api

echo Checking the local AI service...
where ollama >nul 2>nul
if errorlevel 1 (
  echo WARNING: Ollama is not installed. The web app will start, but local AI features need Ollama.
) else (
  curl.exe -fsS --max-time 2 http://127.0.0.1:11434/api/version >nul 2>nul
  if errorlevel 1 (
    echo Ollama is not responding. Trying to start its local server...
    start "AGRO AI - Ollama Server" cmd.exe /k "ollama serve"
    timeout /t 4 /nobreak >nul
    curl.exe -fsS --max-time 2 http://127.0.0.1:11434/api/version >nul 2>nul
    if errorlevel 1 echo WARNING: Ollama is unavailable. Chat and image analysis need Ollama running.
  )
  ollama list 2>nul | findstr /I /C:"qwen2.5vl:3b" >nul
  if errorlevel 1 echo WARNING: qwen2.5vl:3b is missing. Run download_models.bat for image analysis.
  ollama list 2>nul | findstr /I /C:"qwen2.5:1.5b" >nul
  if errorlevel 1 echo WARNING: qwen2.5:1.5b is missing. Run download_models.bat for chat.
)

curl.exe -fsS --max-time 2 http://127.0.0.1:8000/api/health >nul 2>nul
if errorlevel 1 (
  powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
  if not errorlevel 1 (
    echo ERROR: Port 8000 is occupied, but it is not serving the AGRO AI health endpoint.
    goto :fail
  )
  echo Starting backend on port 8000...
  start "AGRO AI Backend" "%~dp0start_backend_windows.bat"
) else (
  echo Backend is already running on port 8000.
)

curl.exe -fsS --max-time 2 http://127.0.0.1:5173/ >nul 2>nul
if errorlevel 1 (
  powershell -NoProfile -Command "if (Get-NetTCPConnection -LocalPort 5173 -State Listen -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }"
  if not errorlevel 1 (
    echo ERROR: Port 5173 is occupied, but it is not serving the AGRO AI frontend.
    goto :fail
  )
  echo Starting frontend on port 5173...
  start "AGRO AI Frontend" "%~dp0start_frontend_windows.bat"
) else (
  echo Frontend is already running on port 5173.
)

echo.
echo Waiting for AGRO AI to become ready...
call :wait_for_api
if errorlevel 1 (
  echo ERROR: Backend did not become ready. Check the AGRO AI Backend window.
  goto :fail
)
call :wait_for_web
if errorlevel 1 (
  echo ERROR: Frontend did not become ready. Check the AGRO AI Frontend window.
  goto :fail
)

echo.
echo AGRO AI is ready:
echo   Web app:        http://localhost:5173
echo   Backend health: http://127.0.0.1:8000/api/health
echo   API docs:       http://127.0.0.1:8000/docs
echo   Ollama status:  http://127.0.0.1:8000/api/ollama/status
echo.
call :open_chrome
echo Keep the AGRO AI Backend and Frontend windows open while using the app.
exit /b 0

:wait_for_api
for /L %%I in (1,1,30) do (
  curl.exe -fsS --max-time 2 http://127.0.0.1:8000/api/health >nul 2>nul
  if not errorlevel 1 exit /b 0
  timeout /t 1 /nobreak >nul
)
exit /b 1

:wait_for_web
for /L %%I in (1,1,30) do (
  curl.exe -fsS --max-time 2 http://127.0.0.1:5173/ >nul 2>nul
  if not errorlevel 1 exit /b 0
  timeout /t 1 /nobreak >nul
)
exit /b 1

:open_chrome
set "CHROME_EXE="
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set "CHROME_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
if not defined CHROME_EXE if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set "CHROME_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
if not defined CHROME_EXE if exist "%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
if defined CHROME_EXE (
  start "" "%CHROME_EXE%" "http://localhost:5173"
) else (
  echo Chrome was not found in its standard install folders. Opening the app in your default browser.
  start "" "http://localhost:5173"
)
exit /b 0

:fail
echo.
echo AGRO AI could not be fully started. Fix the issue above and run start_agro_ai.bat again.
exit /b 1

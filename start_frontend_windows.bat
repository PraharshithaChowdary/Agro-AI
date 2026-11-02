@echo off
cd /d "%~dp0frontend"
title AGRO AI Frontend - Vite
if not exist "node_modules\vite\bin\vite.js" (
  echo ERROR: Frontend dependencies are missing. Run setup_windows.bat first.
  pause
  exit /b 1
)
call npm.cmd run dev -- --host 0.0.0.0
if errorlevel 1 echo Frontend stopped with an error. Read the output above.
pause

@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ===================================================================
echo   AGRO AI - Push Test Suites, Workflows and Excel Reports to GitHub
echo   Repository: https://github.com/PraharshithaChowdary/Agro-AI.git
echo ===================================================================
echo.

git remote set-url origin https://github.com/PraharshithaChowdary/Agro-AI.git

echo Attempting push using Git Credential Manager...
git push -u origin main
if %errorlevel% equ 0 goto success

echo.
echo -------------------------------------------------------------------
echo Note: If GitHub prompted for credentials or gave 403 Permission Denied,
echo you need a GitHub Personal Access Token (PAT) with 'repo' / 'workflow' scope.
echo Create one at: https://github.com/settings/tokens
echo -------------------------------------------------------------------
echo.
set /p GH_TOKEN="Enter your GitHub Personal Access Token (or press ENTER to skip): "

if "%GH_TOKEN%"=="" (
    echo [INFO] No token entered. Please run: git push -u origin main
    goto end
)

echo Pushing with provided token...
git push https://PraharshithaChowdary:%GH_TOKEN%@github.com/PraharshithaChowdary/Agro-AI.git main --force
if %errorlevel% equ 0 goto success

echo.
echo [ERROR] Push failed. Please check the token permissions on GitHub.
goto end

:success
echo.
echo ===================================================================
echo [SUCCESS] Code and GitHub Workflows pushed to GitHub!
echo All 4 test workflows will now run automatically on GitHub Actions.
echo You can download all Excel test reports from:
echo   GitHub Repository -> Actions -> Artifacts -> agro-ai-all-test-excel-reports
echo ===================================================================

:end
pause

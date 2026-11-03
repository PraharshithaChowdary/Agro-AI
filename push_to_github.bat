@echo off
cd /d "c:\Users\praha\Downloads\AGRO_AI_Qwen_Ollama_Codespaces (2)\AGRO_AI_Qwen_Ollama_Codespaces"
echo ========================================================
echo  AGRO AI - Pushing All Passed Test Reports to GitHub
echo  Repository: https://github.com/PraharshithaChowdary/Agro-ai-pdd
echo ========================================================
echo.
git push -u origin main --force
echo.
if %errorlevel% equ 0 (
    echo [SUCCESS] All Excel test reports and project files pushed successfully!
) else (
    echo [ERROR] Push failed. Check error above.
)
pause

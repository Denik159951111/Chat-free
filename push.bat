@echo off
cd /d "%~dp0"
echo ========================================================
echo Pushing NEXUS // AI Chat to GitHub...
echo Repository: https://github.com/Denik159951111/Chat-free.git
echo ========================================================
"C:\Program Files\Git\cmd\git.exe" push -u origin main
echo.
pause

@echo off
title Bridge DigiEval - Batch Registration
echo ============================================
echo   Bridge DigiEval Batch Registration
echo ============================================
echo.

cd /d C:\AutomationProjects\Bridge-Automation.-Framework-
set PYTHONPATH=.

echo Starting batch registration...
echo Logs will appear below. Chrome will open automatically.
echo.
echo Press Ctrl+C at any time to stop.
echo.

python scripts/batch_registration_task.py

echo.
echo ============================================
echo   Batch Registration Completed!
echo ============================================
pause

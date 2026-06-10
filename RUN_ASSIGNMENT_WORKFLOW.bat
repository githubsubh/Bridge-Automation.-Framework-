@echo off
rem -------------------------------------------------------------------
rem Bridge Automation – Full Assignment Workflow Execution Batch
rem -------------------------------------------------------------------
rem This script activates the project's virtual environment and runs the
rem end‑to‑end assignment workflow test.
rem -------------------------------------------------------------------

rem Change directory to the project root (in case script is called from elsewhere)
cd /d "%~dp0"

rem Activate the virtual environment
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo ERROR: Virtual environment not found. Please create it with:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    exit /b 1
)

rem Ensure pytest is installed
pip show pytest >nul 2>&1
if errorlevel 1 (
    echo Installing missing test dependencies...
    pip install -r requirements.txt
)

rem Run the workflow test
python -m pytest tests\workflows\test_assignment_full_workflow.py -s

rem Pause to keep the window open for any error output
pause

exit /b 0

@echo off
rem -------------------------------------------------------------------
rem Bridge Automation – Master Execution Batch
rem -------------------------------------------------------------------
rem This script runs the entire automation suite covering all modules:
rem 1. Admin Portal (Assignment Creation)
rem 2. SME Registration
rem 3. Student Assignment Workflow
rem 4. SME Evaluation Workflow
rem 5. Exam Registration
rem 6. Result/Rechecking/Revaluation
rem -------------------------------------------------------------------

cd /d "%~dp0"

echo ========================================================
echo Bridge Automation Framework - Full Suite Execution
echo ========================================================

rem Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo ERROR: Virtual environment not found. Please create it first.
    exit /b 1
)

echo.
echo Running full automation suite...
echo.

rem Run pytest with all relevant modules
python -m pytest tests/admin/test_admin_assignment_creation.py tests/admin/test_sme_self_registration.py tests/test_student_assignment_workflow.py tests/test_sme_evaluation_workflow.py tests/exam/test_exam_registration.py tests/test_result_rechecking.py -s -v --html=reports/full_suite_report.html

echo.
echo ========================================================
echo Execution Completed. Check reports folder for details.
echo ========================================================

pause
exit /b 0

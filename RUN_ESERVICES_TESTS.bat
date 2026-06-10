@echo off
title Bridge - E-Services Automation Suite
color 0B

:menu
cls
echo ============================================================
echo   BRIDGE - E-SERVICES AUTOMATION GATEWAY
echo ============================================================
echo.
echo   Please select the E-Services test suite to execute:
echo.
echo   [1] Run Dynamic Functional E-Services Suite (test_eservices_fixed.py - Checks All Services)
echo   [2] Run Negative Form Validation Suite (test_eservices_negative.py)
echo   [3] Run Both Test Suites (Sequential Execution)
echo   [4] Exit Gateway
echo.
echo ============================================================
set /p choice="Enter your choice [1-4]: "

if "%choice%"=="1" goto functional
if "%choice%"=="2" goto negative
if "%choice%"=="3" goto both
if "%choice%"=="4" goto exit
goto menu

:functional
cls
echo ============================================================
echo   RUNNING: DYNAMIC FUNCTIONAL E-SERVICES SUITE (CHECKS ALL E-SERVICES)
echo ============================================================
echo.
echo  [IMPORTANT CAPTCHA NOTICE]:
echo  1. A Chrome browser window will automatically launch.
echo  2. The script will enter the Email and Password automatically.
echo  3. PLEASE WATCH the browser, manually type the CAPTCHA image,
echo     and click the 'Login' button.
echo  4. The automation script will wait up to 120 seconds for you 
echo     to complete this login before automated testing begins!
echo.
echo ============================================================
echo.
cd /d "%~dp0"
set PYTHONPATH=.
.venv\Scripts\pytest tests/test/eservices/test_eservices_fixed.py -s
goto end

:negative
cls
echo ============================================================
echo   RUNNING: NEGATIVE E-SERVICES VALIDATION SUITE
echo ============================================================
echo.
echo  [IMPORTANT CAPTCHA NOTICE]:
echo  1. A Chrome browser window will automatically launch.
echo  2. The script will enter the Email and Password automatically.
echo  3. PLEASE WATCH the browser, manually type the CAPTCHA image,
echo     and click the 'Login' button.
echo  4. The automation script will wait up to 120 seconds for you 
echo     to complete this login before automated testing begins!
echo.
echo ============================================================
echo.
cd /d "%~dp0"
set PYTHONPATH=.
.venv\Scripts\pytest tests/test/eservices/test_eservices_negative.py -s
goto end

:both
cls
echo ============================================================
echo   RUNNING: BOTH E-SERVICES SUITES
echo ============================================================
echo.
echo  [IMPORTANT CAPTCHA NOTICE]:
echo  1. A Chrome browser window will automatically launch.
echo  2. The script will enter the Email and Password automatically.
echo  3. PLEASE WATCH the browser, manually type the CAPTCHA image,
echo     and click the 'Login' button.
echo  4. The automation script will wait up to 120 seconds for you 
echo     to complete this login before automated testing begins!
echo.
echo ============================================================
echo.
cd /d "%~dp0"
set PYTHONPATH=.
echo [INFO] Running Functional suite first...
.venv\Scripts\pytest tests/test/eservices/test_eservices_fixed.py -s
echo.
echo [INFO] Running Negative Validation suite next...
.venv\Scripts\pytest tests/test/eservices/test_eservices_negative.py -s
goto end

:end
echo.
echo ============================================================
echo   Execution Completed!
echo   Report generated under: docs/executions/
echo ============================================================
echo.
pause
goto menu

:exit
cls
echo Thank you for using Bridge Automation. Exiting...
timeout /t 2 >nul
exit

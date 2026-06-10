@echo off
echo ===================================================
echo   RUNNING BRIDGE AUTOMATION TEST SUITE (ORDERED)
echo ===================================================

REM 1. Registration (Test_001)
echo [1/5] Running Registration Tests...
python -m pytest tests/test/registration --browser chrome

REM 2. Login (Test_002)
echo [2/5] Running Login Tests...
python -m pytest tests/test/auth/test_login.py --browser chrome

REM 3. Dashboard Features (Test_003, 004, 005, 007, 010, 011, 012)
echo [3/5] Running Dashboard Tests...
python -m pytest tests/test/dashboard --browser chrome

REM 4. E-Services (Test_006, 008)
echo [4/5] Running E-Services Tests...
python -m pytest tests/test/eservices --browser chrome

REM 5. Logout (Test_009)
echo [5/5] Running Logout Tests...
python -m pytest tests/test/auth/test_logout.py --browser chrome

echo ===================================================
echo   TEST SUITE EXECUTION COMPLETE
echo ===================================================
pause

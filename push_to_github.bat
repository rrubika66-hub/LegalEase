@echo off
setlocal
echo ======================================================================
echo    LegalEase: Pushing to https://github.com/rrubika66-hub/LegalEase.git
echo ======================================================================
echo.

set "GIT_EXE=C:\Users\ELCOT\.gemini\antigravity-ide\scratch\mingit\cmd\git.exe"

if exist "%GIT_EXE%" (
    set "GIT_CMD=%GIT_EXE%"
) else (
    set "GIT_CMD=git"
)

echo Using Git binary at: %GIT_CMD%
echo.

"%GIT_CMD%" remote remove origin 2>nul
"%GIT_CMD%" remote add origin https://github.com/rrubika66-hub/LegalEase.git
"%GIT_CMD%" branch -M main

echo Pushing all 27 files to GitHub...
"%GIT_CMD%" push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Your project is now live on GitHub!
    echo Visit: https://github.com/rrubika66-hub/LegalEase
    echo ======================================================================
) else (
    echo [INFO] If a GitHub login window opened, complete the authorization.
)
pause

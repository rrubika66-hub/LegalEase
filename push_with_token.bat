@echo off
setlocal
echo ======================================================================
echo    LegalEase: Quick Push to GitHub (with Token Support)
echo ======================================================================
echo Target Repo: https://github.com/rrubika66-hub/LegalEase.git
echo.

set "GIT_EXE=C:\Users\ELCOT\.gemini\antigravity-ide\scratch\mingit\cmd\git.exe"
if exist "%GIT_EXE%" (
    set "GIT_CMD=%GIT_EXE%"
) else (
    set "GIT_CMD=git"
)

echo Option 1: Standard Push (Browser / Credential Manager Authentication)
echo Option 2: Push using GitHub Personal Access Token (PAT)
echo.
set /p CHOICE="Select option (1 or 2): "

if "%CHOICE%"=="2" (
    echo.
    set /p GITHUB_TOKEN="Enter your GitHub Personal Access Token (ghp_...): "
    if defined GITHUB_TOKEN (
        "%GIT_CMD%" remote remove origin 2>nul
        "%GIT_CMD%" remote add origin https://rrubika66-hub:%GITHUB_TOKEN%@github.com/rrubika66-hub/LegalEase.git
        "%GIT_CMD%" branch -M main
        "%GIT_CMD%" push -u origin main
    ) else (
        echo [ERROR] Token cannot be empty.
    )
) else (
    "%GIT_CMD%" remote remove origin 2>nul
    "%GIT_CMD%" remote add origin https://github.com/rrubika66-hub/LegalEase.git
    "%GIT_CMD%" branch -M main
    "%GIT_CMD%" push -u origin main
)

echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo [SUCCESS] Your project has been uploaded to GitHub!
    echo Visit: https://github.com/rrubika66-hub/LegalEase
    echo ======================================================================
) else (
    echo [INFO] If prompted, sign in through your browser to grant access.
)
pause

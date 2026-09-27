@echo off
setlocal enabledelayedexpansion
echo ======================================================================
echo    LegalEase: Automatic Push to https://github.com/rrubika66-hub/LegalEase.git
echo ======================================================================
echo.

REM Add standard Git install directories to PATH if not already present
set "PATH=%PATH%;C:\Program Files\Git\cmd;C:\Program Files\Git\bin;C:\Users\%USERNAME%\AppData\Local\Programs\Git\cmd"

REM Check if git is recognized
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not recognized in PATH.
    echo Please ensure Git is installed, or restart your Command Prompt.
    pause
    exit /b 1
)

echo [1/5] Checking Git repository initialization...
if not exist ".git" (
    git init
)

echo [2/5] Setting branch to main...
git branch -M main

echo [3/5] Staging all files...
git add .

echo [4/5] Creating commit...
git commit -m "feat: complete production release of LegalEase AI Legal Document Generator" || echo No changes to commit.

echo [5/5] Configuring remote origin and pushing...
git remote remove origin 2>nul
git remote add origin https://github.com/rrubika66-hub/LegalEase.git

echo.
echo Pushing to GitHub (https://github.com/rrubika66-hub/LegalEase.git)...
git push -u origin main

echo.
echo ======================================================================
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Your project is now live at:
    echo https://github.com/rrubika66-hub/LegalEase
) else (
    echo If prompted, please complete the GitHub sign-in in your browser or enter your GitHub Personal Access Token.
)
echo ======================================================================
pause

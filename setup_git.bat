@echo off
echo ======================================================================
echo          LegalEase: Git Repository Initialization & Setup
echo ======================================================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/downloads and rerun this script.
    pause
    exit /b 1
)

REM Initialize repository if not already initialized
if not exist ".git" (
    echo [1/4] Initializing new Git repository...
    git init
) else (
    echo [1/4] Existing Git repository detected.
)

REM Check if user is configured
git config user.name >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Setting default local git username...
    git config user.name "LegalEase Developer"
    git config user.email "dev@legalease.ai"
)

REM Ensure default branch is main
git branch -M main

REM Stage all project files (respecting .gitignore)
echo [2/4] Staging project files...
git add .

REM Commit changes
echo [3/4] Creating semantic initial commit...
git commit -m "feat: complete production release of LegalEase AI Legal Document Generator"

echo.
echo ======================================================================
echo [4/4] Git initialization complete!
echo ======================================================================
echo.
echo To link and push this repository to GitHub, run:
echo.
echo    1. Create a new repository on GitHub: https://github.com/new
echo    2. Run the following commands in this directory:
echo.
echo       git remote add origin https://github.com/YOUR_USERNAME/LegalEase.git
echo       git push -u origin main
echo.
echo ======================================================================
pause

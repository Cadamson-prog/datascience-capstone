@echo off
rem Bootstrap the Python environment for this repo. Safe to re-run.
rem Mirrors steps 1-3 of docs\DEVELOPER_SETUP.md (venv create, install
rem requirements.txt, editable install of the project package).
setlocal

cd /d "%~dp0"

set VENV_DIR=.venv
set PROMPT=datascience-capstone

if exist "%VENV_DIR%" (
    echo [devsetup] %VENV_DIR%\ already exists, skipping venv creation.
) else (
    echo [devsetup] Creating virtual environment in %VENV_DIR%\ ...
    python -m venv "%VENV_DIR%" --prompt "%PROMPT%"
    if errorlevel 1 exit /b %ERRORLEVEL%
)

set PIP=%VENV_DIR%\Scripts\pip.exe
set PYTHON=%VENV_DIR%\Scripts\python.exe

echo [devsetup] Upgrading pip ...
"%PYTHON%" -m pip install --upgrade pip
if errorlevel 1 exit /b %ERRORLEVEL%

echo [devsetup] Installing requirements.txt ...
"%PIP%" install -r requirements.txt
if errorlevel 1 exit /b %ERRORLEVEL%

echo [devsetup] Installing project as editable package ...
"%PIP%" install -e .
if errorlevel 1 exit /b %ERRORLEVEL%

echo.
echo [devsetup] Done. Activate the venv in your shell with:
echo     %VENV_DIR%\Scripts\activate

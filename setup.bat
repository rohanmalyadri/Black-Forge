@echo off
REM One-command setup for Black Forge on Windows.
REM Made with love Rohan Malyadri From Obscuron X Labs
setlocal
cd /d "%~dp0"
echo === Black Forge setup ===

REM 1. Find Python 3.10+ (prefer the "py" launcher that python.org installs)
set "PY="
for %%V in (3.13 3.12 3.11 3.10) do (
  if not defined PY (
    py -%%V -c "import sys" >nul 2>&1 && set "PY=py -%%V"
  )
)
if not defined PY (
  python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1 && set "PY=python"
)
if not defined PY (
  echo ERROR: Black Forge needs Python 3.10 or newer, and none was found.
  echo Install it from https://www.python.org/downloads/ ^(tick "Add python.exe to PATH"^), then run setup.bat again.
  exit /b 1
)
echo Using %PY%

REM 2. Virtual environment + dependencies
if not exist ".venv\Scripts\python.exe" (
  %PY% -m venv .venv || (echo ERROR: could not create a virtual environment. & exit /b 1)
)
".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip
echo Installing dependencies (first run takes a minute)...
".venv\Scripts\python.exe" -m pip install --quiet -r requirements.txt || (echo ERROR: dependency install failed. & exit /b 1)

REM 3. API key
if not exist ".env" (
  copy /y ".env.example" ".env" >nul
  set /p "KEY=Paste your Gemini API key (https://aistudio.google.com/apikey), or press Enter to add it later: "
)
if defined KEY (
  ".venv\Scripts\python.exe" -c "import sys; p='.env'; s=open(p).read().replace('your_gemini_api_key_here', sys.argv[1].strip()); open(p,'w').write(s)" "%KEY%"
)

echo.
echo Done! Try:
echo   blackforge about
echo   blackforge chat "List the files in this folder"
echo   blackforge optimize --goal "Launch Black Forge" --platform LinkedIn --draft "Black Forge is an AI agent for your terminal."
endlocal

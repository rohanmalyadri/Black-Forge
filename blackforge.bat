@echo off
REM Black Forge launcher for Windows: works without activating the virtual environment.
setlocal
set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo Black Forge is not installed yet. Run setup.bat first.
  exit /b 1
)
if /i "%~1"=="optimize" (
  shift
  goto optimize
)
"%PY%" -m black_forge %*
exit /b %errorlevel%

:optimize
set "ARGS="
:collect
if "%~1"=="" goto run
set ARGS=%ARGS% %1
shift
goto collect
:run
"%PY%" "%~dp0main.py" %ARGS%
exit /b %errorlevel%

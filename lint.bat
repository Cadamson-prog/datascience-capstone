@echo off
rem Convenience wrapper that runs both linting scripts:
rem   - src/scripts/linting/py_lint.py  (Python files)
rem   - src/scripts/linting/nb_lint.py  (Jupyter notebooks)
rem Locates the scripts relative to this file, so it runs the same way from any
rem working directory. Any arguments are forwarded to both scripts.

python "%~dp0src\scripts\linting\py_lint.py" %*
if errorlevel 1 exit /b %ERRORLEVEL%

python "%~dp0src\scripts\linting\nb_lint.py" %*
exit /b %ERRORLEVEL%

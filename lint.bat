@echo off
rem Convenience wrapper for src/scripts/linting/py_lint.py.
rem Locates the script relative to this file, so it runs the same way from any
rem working directory. Any arguments are forwarded to py_lint.py.

python "%~dp0src\scripts\linting\py_lint.py" %*
exit /b %ERRORLEVEL%

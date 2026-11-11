@echo off
REM Claude Code Plugins Hub - Windows Command Prompt Setup
cd /d "%~dp0"

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python install.py
    goto end
)

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py install.py
    goto end
)

echo [EROARE] Python nu este instalat sau nu se gaseste in PATH!
echo Descarca Python de la https://python.org si asigura-te ca bifezi "Add Python to PATH".
pause
exit /b 1

:end
pause

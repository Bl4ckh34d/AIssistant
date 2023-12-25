@echo off
set "INSTALL_DIR=%~dp0"
set "PYTHON=%INSTALL_DIR%\env\python.exe"
set "ENV=%INSTALL_DIR%\env"
set "SCRIPTS_DIR=%INSTALL_DIR%\scripts"

wt -w 0 -d %SCRIPTS_DIR% --title "Main Program" cmd /k "call conda activate %ENV% && %PYTHON% main.py" 2> nul
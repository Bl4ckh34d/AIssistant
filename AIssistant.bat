@echo off
set PYTHON=D:\AI\env\python.exe
set ENV=D:\AI\env

wt -w 0 -d "D:\AI\scripts" --title "Main Program" cmd /k "call conda activate %ENV% && %PYTHON% main.py" 2> nul
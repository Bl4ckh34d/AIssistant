@echo off
set PYTHON=D:\AI\env\python.exe
set ENV=D:\AI\env

wt -w 0 -d "D:\AI\webui" --title "AI Server" cmd /k "call conda activate %ENV% && %PYTHON% server.py --verbose --model airoboros-l2-7b-2.1.ggmlv3.Q4_K_M --extensions api --loader llama.cpp --xformers"

timeout /t 3 /nobreak > nul

wt -w 0 -d "D:\AI\scripts" --title "Main Program" cmd /k "call conda activate %ENV% && %PYTHON% main.py"
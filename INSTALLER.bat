@echo off
setlocal

set /p manual_paths="Type 'y' to enter installation and model paths manually: "

set "install_path=D:\AI"
set "path_to_model=D:\airoboros-l2-7b-2.1.ggmlv3.Q4_K_M"

if manual_paths=="y" (
	set /p install_path="Enter Path to installation directory: "
	set /p path_to_model="Enter Path to model files: "
)
if manual_paths=="yes" (
	set /p install_path="Enter Path to installation directory: "
	set /p path_to_model="Enter Path to model files: "
)

set "env_path=%install_path%\env"
set "webui_path=%install_path%\webui"
set "model_path=%webui_path%\models"

if not exist "%install_path%" (
    mkdir "%install_path%"
    echo Directory "%install_path%" created successfully.
) else (
    echo Directory "%install_path%" already exists.
)

cd %install_path% && ^
conda create -p %env_path% python==3.10.11 pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y && ^
conda activate %env_path% && ^
git clone https://github.com/oobabooga/text-generation-webui && ^
ren "text-generation-webui" "webui" && ^
cd %webui_path% && ^
pip install -r requirements.txt && ^
pip install click werkzeug pyaudio sounddevice soundfile TTS xformers && ^
pip install -U openai-whisper && ^
pip install pywinauto && ^
move %path_to_model% %model_path% && ^
pause

endlocal
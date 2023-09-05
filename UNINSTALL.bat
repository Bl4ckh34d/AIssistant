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

conda deactivate && ^
conda uninstall -p %env_path% --all -y && ^
cd %model_path% && ^
move airoboros-l2-7b-2.1.ggmlv3.Q4_K_M %path_to_model% && ^
cd %install_path% && ^
rmdir /s /q webui && ^
pause

endlocal
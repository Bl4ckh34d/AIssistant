# AIssistant
A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.

*INSTALL with oobabooga already cloned to "webui":*
conda create -p D:\AI\env python==3.10.6 -y ^
&& conda activate D:\AI\env ^
&& cd D:\AI\webui ^
&& pip3 install -r requirements.txt ^
&& pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -y

*INSTALL completely:*
conda create -p D:\AI\env python==3.10.6 -y && ^
conda activate D:\AI\env && ^
cd D:\AI && ^
git clone https://github.com/oobabooga/text-generation-webui && ^
ren "text-generation-webui" "webui" && ^
cd D:\AI\webui && ^
pip3 install -r requirements.txt && ^
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 -y

*UNINSTALL Conda environment:*
conda deactivate && ^
conda uninstall -p D:\AI\env --all -y
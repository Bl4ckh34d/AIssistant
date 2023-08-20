# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.

## INSTALL with oobabooga already cloned to "webui":

conda create -p D:\AI\env python==3.10.11 -y && ^
conda activate D:\AI\env && ^
d: && ^
cd D:\AI\webui && ^
pip3 install -r requirements.txt && ^
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && ^
pip3 install pyaudio && ^
pip3 install sounddevice && ^
pip3 install soundfile && ^
pip3 install TTS && ^
pip3 install xformers && ^
pip3 install -U openai-whisper

## INSTALL completely:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch

conda create -p D:\AI\env python==3.10.11 -y && ^
conda activate D:\AI\env && ^
d: && ^
cd D:\AI && ^
git clone https://github.com/oobabooga/text-generation-webui && ^
ren "text-generation-webui" "webui" && ^
cd D:\AI\webui && ^
pip3 install -r requirements.txt && ^
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 && ^
pip3 install pyaudio && ^
pip3 install sounddevice && ^
pip3 install soundfile && ^
pip3 install TTS && ^
pip3 install xformers && ^
pip3 install -U openai-whisper

## UNINSTALL Conda environment:*

conda deactivate && ^
conda uninstall -p D:\AI\env --all -y
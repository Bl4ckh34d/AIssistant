# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.

## INSTALL:
Pytorch:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch


conda create -p D:\AI\env python==3.10.11 pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y && ^<br>
conda activate D:\AI\env && ^<br>
d: && ^<br>
cd D:\AI && ^<br>
git clone https://github.com/oobabooga/text-generation-webui && ^<br>
ren "text-generation-webui" "webui" && ^<br>
cd D:\AI\webui && ^<br>
pip3 install -r requirements.txt && ^<br>
pip3 install click werkzeug pyaudio sounddevice soundfile TTS xformers && ^<br>
pip3 install -U openai-whisper && ^<br>
mkdir "D:\AI\webui\models\airoboros-l2-7b-gpt4-2.0.ggmlv3.q4_K_S"

Model:
- https://huggingface.co/TheBloke/airoboros-l2-7B-gpt4-2.0-GGML/blob/main/airoboros-l2-7b-gpt4-2.0.ggmlv3.q4_K_S.bin
- https://huggingface.co/TheBloke/airoboros-l2-7B-gpt4-2.0-GGML/blob/main/config.json

## UNINSTALL Conda environment:*

conda deactivate && ^<br>
conda uninstall -p D:\AI\env --all -y && ^<br>
d: && ^<br>
cd D:\AI\webui\models\ && ^<br>
mv airoboros-l2-7b-gpt4-2.0.ggmlv3.q4_K_S D:\ && ^<br>
rmdir /s /q webui
# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.

## INSTALL for usage:
Pytorch:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch

```shell
conda create -p D:\AI\env python==3.10.11 pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y && ^
conda activate D:\AI\env && ^
d: && ^
cd D:\AI && ^
git clone https://github.com/oobabooga/text-generation-webui && ^
ren "text-generation-webui" "webui" && ^
cd D:\AI\webui && ^
pip3 install -r requirements.txt && ^
pip3 install click werkzeug pyaudio sounddevice soundfile TTS xformers && ^
pip3 install -U openai-whisper && ^
move D:\airoboros-l2-7b-gpt4-2.0.ggmlv3.q4_K_S D:\AI\webui\models\ || echo "Cannot move model into 'webui/models'"
```

Model:
- https://huggingface.co/TheBloke/airoboros-l2-7B-gpt4-2.0-GGML/blob/main/airoboros-l2-7b-gpt4-2.0.ggmlv3.q4_K_S.bin
- https://huggingface.co/TheBloke/airoboros-l2-7B-gpt4-2.0-GGML/blob/main/config.json

## UNINSTALL for Github committing and pushing:

```shell
conda deactivate && ^
conda uninstall -p D:\AI\env --all -y && ^
d: || echo "Skipping moving to D: drive" && ^
cd D:\AI\webui\models\ || echo "Skipping moving to D:\AI\webui\models\" && ^
move airoboros-l2-7b-gpt4-2.0.ggmlv3.q4_K_S D:\ || echo "Cannot evacuate model to D: drive" && ^
rmdir /s /q webui || echo "Cannot remove 'webui'"
```
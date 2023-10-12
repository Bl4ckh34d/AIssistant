# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.

## INSTALL for usage:
Pytorch:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch

Conda:
- https://docs.conda.io/projects/miniconda/en/latest/ is where you can find the current version of conda. THIS IS REQUIRED for the following install script. Paths also need to be adapted for your environment:

```shell
install_path="D:\AI\env"
path_to_model="D:\airoboros-l2-7b-2.1.ggmlv3.Q4_K_M"

env_path="$install_path\env"
webui_path="$install_path\webui"
model_path="$webui_path\models"

mkdir -p "$install_path" && ^
cd $install_path && ^
conda create -p $env_path python==3.10.11 pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y && ^
conda activate $env_path && ^
git clone https://github.com/oobabooga/text-generation-webui && ^
ren "text-generation-webui" "webui" && ^
cd "$webui_path" && ^
pip3 install -r requirements.txt && ^
pip3 install click werkzeug pyaudio sounddevice soundfile TTS xformers && ^
pip3 install -U openai-whisper && ^
pip3 install pyautogui && ^
move $path_to_model $model_path
```

Models I used for testing:
LLM:
- https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/blob/main/mistral-7b-openorca.Q4_K_M.gguf
- https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/resolve/main/config.json

SA:
- cardiffnlp--twitter-roberta-base-sentiment-latest

STT:
- whisper (small)

TTS:
- tts_models--en--jenny--jenny
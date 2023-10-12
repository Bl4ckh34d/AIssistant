# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.
- Rudimentary Mood System: User and LLMs messages are put through Sentiment Analysis and rated positive or negative, influencing the AIs mood (BARELY TESTED)
- Rudimentary Longterm-Memory: Based on past chat logs, the LLM fills its context with chats older than 5 days, chats within the last 5 days and the most recent conversation. (UNTESTED)

NOTE: Expect crashes and errors, features not working and all sorts of bugs, as this is VERY WIP.

## REQUIREMENTS:
Pytorch:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch

Conda:
- https://docs.conda.io/projects/miniconda/en/latest/ is where you can find the current version of conda. THIS IS REQUIRED for the following install script. Paths also need to be adapted for your environment:


## INSTALLATION:
Copy the following text block as a whole into your terminal and confirm. It SHOULD work.

```shell
install_path="D:\AI\env"
env_path="$install_path\env"
webui_path="$install_path\webui"

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
pip3 install pyautogui
```

Models I used for testing:
LLM:
- https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/blob/main/mistral-7b-openorca.Q4_K_M.gguf
- https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/resolve/main/config.json

SA:
- https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest/tree/main

STT:
- whisper (small) (should download automatically once started)

TTS:
- tts_models--en--jenny--jenny (should download automatically once started)
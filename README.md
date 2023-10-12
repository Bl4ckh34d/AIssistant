# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.
- Rudimentary Mood System: User and LLMs messages are put through Sentiment Analysis and rated positive or negative, influencing the AIs mood (BARELY TESTED)
- Rudimentary Longterm-Memory: Based on past chat logs, the LLM fills its context with chats older than 5 days, chats within the last 5 days and the most recent conversation. (UNTESTED)

TODO:
- Different colors in Terminal for User Messages and LLM Messages
- Including date and time into Chat history json
- Finding better prompts for the currently used LLM
- Browser Extensions (Chrome and Firefox) for remote control through LLM
- Include an easy option to turn the LLM reply on and off
- Continue recording the user input and transcribing sentence by sentence. When sending these chunks to the LLM, collect them temporarily until the LLM finished replying.
All this in parallel with the TTS, which currently blocks the whole loop until it is done speaking.

NOTE: Expect crashes and errors, features not working and all sorts of bugs, as this is VERY WIP.
Also note, that not the answer of the LLM is responsible for triggering functions and tasks on the users mashine but the users transcribed voice input.
This way it was more reliable to trigger functions and also much faster than waiting for the LLM to reply.

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
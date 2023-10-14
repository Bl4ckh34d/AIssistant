# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.
- Rudimentary Mood System: User and LLMs messages are put through sentiment analysis and rated positive or negative, influencing the AIs mood (BARELY TESTED)
- Rudimentary Longterm-Memory: Based on past chat logs, the LLM fills its context with chats older than 5 days, chats within the last 5 days and the most recent conversation. (UNTESTED)
- Shortterm-Memory should clean itself before reaching the token maximum

## NOTICE!:
- I created this for myself in a private capacity and non-commercially. It is not well tested, nor professionally built. **USE ON YOUR OWN RISK!!**
- Expect CRASHES, ERRORS and features NOT working correctly, as this is VERY WIP and dependent on your OS. Adjust the paths in [commands.py](https://github.com/Bl4ckh34d/AIssistant/blob/5f7ef44548ab6323a588dc9b6d2560adafca794d/scripts/commands.py#L13-L30) to your needs. This script as well as [commands_list.py](https://github.com/Bl4ckh34d/AIssistant/blob/main/scripts/command_list.py) are interesting for you, if you want to add your own functionality. Saving and deleting files is currently not implemented for safety reasons. Also a more fine-grained control still needs to be worked out to give multiple commands in a single sentence or two.
- Also note, that not the answer of the LLM is responsible for triggering functions and tasks on the users mashine. The users transcribed voice input is used for this.
This way it was more reliable to trigger functions and also much faster than waiting for the LLM to reply.
- If you really wish for the LLM to be responsible for executing the commands, simply trigger the responsible function using the LLM response as argument. But you will have to instruct the LLM to answer in a certain way to your requests so it triggers the execution of the tasks. I changed this
to the voice input of the user because this method was very unreliable. Possibly this will be changed back to the LLM once models become more reliable and consistent.

The whole system is setup to work with VirtualCable and VRTuber if you wish for a little AI avatar that animates its mouth to the TTS output. In VRTuber you also need to setup the virtual microphone and possibly change the ID for the virtual audio device in the [variables.py](https://github.com/Bl4ckh34d/AIssistant/blob/f00a99d99926e7cfc207a599556aefc3d43c634d/scripts/variables.py#L155). Run [device_test.py](https://github.com/Bl4ckh34d/AIssistant/blob/main/scripts/device_test.py) to see the IDs of your audio devices.

## USAGE:
First you might want to adjust the user_name and ai_name, ai_gender, the paths to your programs and some other things inside [variables.py](https://github.com/Bl4ckh34d/AIssistant/blob/ac081c086708e21e9cc5ef2cf7832181d124d44b/scripts/variables.py#L75-L78).

**Currently implemented voice commands:**

#### AGAIN
> The word 'again' in a sentence without any of the other keywords will trigger the last action once more.
#### GO BACK... (BY ONE)
##### ...TAB
> This should switch back by one tab
#### SCROLL...
##### ...UP
> This should scroll the current active window up a fair bit.
##### ...DOWN
> This should scroll the current active window down a fair bit.
#### GO TO...
> 'Go to' followed by a process name or folder should bring that folder/process to the foreground if it is currently open.
#### OPEN...
> This followed by a program or '...new folder at (Folder Location) should open the programm or folder at said location.
##### ...NEW FOLDER TAB AT (FOLDER LOCATION)
> Opens a new tab in the currently active folder at the requested folder location
##### ...NEW TAB
> Opens a new browser or program tab
#### CLOSE...
##### ...WINDOW/TAB/etc.
> Should close the requested thing
#### SWITCH...
##### ...WINDOW/TAB
#### MINIMIZE...
> Minimizes active window
#### MAXIMIZE...
> Maximizes active window
#### REFRESH...
> Same as hitting F5 on the keyboard

#### FOLDER LOCATIONS:
- C Drive
- D Drive
- AppData
- Programs
- Programs86
- Home
- Downloads

#### PROGRAMS:
- Firefox
- Firefox (Incognito)
- Explorer
- VLC
- Media Player Classic
- Keepass
- Steam
- Discord
- MS Word
- MS Excel
- MS Powerpoint
- Notepad++
- VSC
- PureRef
- Audacity
- Blender
- Stable Diffusion
- Calculator
- System Settings

## TODO:
- Including date and time into chat history .json
- Find better prompts for the currently used LLM (Mistral-7b-OpenOrca)
- Browser extensions (Chrome and Firefox) for remote control through LLM
- Include an easy option to turn the LLM reply on and off
- Continue recording the user input and transcribing sentence by sentence. When sending these chunks to the LLM, collect them temporarily until the LLM finished replying.
All this in parallel with the TTS, which currently blocks the whole loop until it is done speaking.
- Possibly integrate Open Interpreter and ditch my own execution code completely, if OI integrates well into this program.

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
pip3 install colorama
```

*Models I used for testing:*

LLM:
- https://huggingface.co/TheBloke/dolphin-2.1-mistral-7B-GGUF/resolve/main/dolphin-2.1-mistral-7b.Q4_K_M.gguf
- https://huggingface.co/TheBloke/dolphin-2.1-mistral-7B-GGUF/resolve/main/config.json

SA:
- https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest/tree/main

STT:
- whisper (small) (should download automatically once started)

TTS:
- tts_models--en--jenny--jenny (should download automatically once started)

## If you enjoy what I make, consider buying me a coffee for all these sleepless nights coding away :)
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/danielbenew)
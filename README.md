# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.
- Rudimentary Mood System: User and LLMs messages are put through sentiment analysis and rated positive or negative, influencing the AIs mood (BARELY TESTED)
- Rudimentary Longterm-Memory: Based on past chat logs, the LLM fills its context with chats older than 5 days, chats within the last 5 days and the most recent conversation. (UNTESTED)
- Shortterm-Memory should clean itself before reaching the token maximum

## NOTICE!:
- I created this for myself in a private capacity and not for commercial use. It is not well tested, nor professionally built and the model prompt is TOXIC!
- This is WIP and might not work as expected.
- Adjust the paths in [commands.py](https://github.com/Bl4ckh34d/AIssistant/blob/5f7ef44548ab6323a588dc9b6d2560adafca794d/scripts/commands.py#L13-L30) to your needs. This script as well as [commands_list.py](https://github.com/Bl4ckh34d/AIssistant/blob/main/scripts/command_list.py) are interesting for you, if you want to add your own functionality. Saving and deleting files is currently not implemented for safety reasons. Also a more fine-grained control still needs to be worked out to give multiple commands in a single sentence.
- Also note, that not the answer of the LLM is responsible for triggering functions and tasks on the users mashine. The users transcribed voice input is used for this. This way it is more reliable to trigger functions and also faster than waiting for the LLM to get it right.
- If you really wish for the LLM to be responsible for executing the commands, simply trigger the responsible function using the LLM response as argument. But you will have to instruct the LLM to answer in a certain way to your requests so it triggers the execution of the tasks. I changed this
to the voice input of the user because this method was very unreliable. Possibly this will be changed back to the LLM once models become more reliable and consistent.

The whole system is setup to work with VirtualCable and VRTuber if you wish for a little AI avatar that animates its mouth to the TTS output. In VRTuber you also need to setup the virtual microphone and possibly change the ID for the virtual audio device in the [variables.py](https://github.com/Bl4ckh34d/AIssistant/blob/f00a99d99926e7cfc207a599556aefc3d43c634d/scripts/variables.py#L155). Run [device_test.py](https://github.com/Bl4ckh34d/AIssistant/blob/main/scripts/device_test.py) to see the IDs of your audio devices.

## USAGE:
First you might want to adjust the paths to your programs and some other things inside [variables.py](https://github.com/Bl4ckh34d/AIssistant/blob/ac081c086708e21e9cc5ef2cf7832181d124d44b/scripts/variables.py#L75-L78).

```Start AIssistant.bat```

Enjoy talking to your very own AI Assistant. Tell the AI to open Firefox, close the tab or maximize the window, etc.

#### **Currently implemented voice commands to trigger actions:**
- **AGAIN**: The word 'again' in a sentence without any of the other keywords will trigger the last action once more.)
- **GO BACK...** followed by **...TAB**: This should switch back by one tab
- **SCROLL...** followed by **...UP**: This should scroll the current active window up a fair bit.
- **SCROLL...** followed by **...DOWN**: This should scroll the current active window down a fair bit.
- **GO TO...**: This followed by a process name or folder should bring that folder/process to the foreground if it is currently open.
- **OPEN...**: This followed by a program or '...new folder at (Folder Location) should open the programm or folder at said location.
- **...NEW FOLDER TAB AT (FOLDER LOCATION)**: Opens a new tab in the currently active folder at the requested folder location
- **...NEW TAB**: Opens a new browser or program tab
- **CLOSE...** followed by **...WINDOW/TAB/**etc.: This Should close the requested window, tab or process
- **SWITCH...** followed by **..WINDOW/TAB**: Equivalent to pressing ALT + Tab
- **MINIMIZE...**: Minimizes active window
- **MAXIMIZE...**: Maximizes active window
- **REFRESH...**: Same as hitting F5 on the keyboard

#### **FOLDER LOCATIONS**:
C Drive, D Drive, AppData, Programs, Programs86, Home, Downloads

#### **CURRENTLY SUPPORTED PROGRAMS**:
Firefox, Firefox (Incognito), Explorer, VLC, Media Player Classic, Keepass, Steam, Discord, MS Word, MS Excel, MS Powerpoint, Notepad++,
VSC, PureRef, Audacity, Blender, Stable Diffusion, Calculator, System Settings

## TODO:
- Sentiment Score of LLM seems to not work as expected, need to revisit
- Browser extensions (Chrome and Firefox) for remote control through LLM
- Implement Youtube API / Google API / ChatGPT API
- Include an easy option to turn the LLM reply on and off
- Possibly integrate Open Interpreter and ditch my own code execution completely at some point, if OI integrates well into this.
- Since I don't use LangChain but rather built my own Longterm Memory System, I still need to implement the following things:
  - Once a json-Log is finished (current date =/= log date), and thie file is selected randomly to be in the memory, the LLM should add a summary of the conversation to the file. (skip this step if the summary is already in there).
- Writing a scraper for search engines, wikipedia, weather forecast, etc. or giving the LLM API access to services for current information.
- Getting a embedding model (maybe sentence-transformers/all-MiniLM-L6-v2) to process outside information from Vector Index (pinecone-like but locally?) + embedding dataset

## REQUIREMENTS:
Pytorch:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch

Miniconda:
- https://docs.conda.io/projects/miniconda/en/latest/ is where you can find the current version of conda. THIS IS REQUIRED for the following install script. Paths also need to be adapted for your environment:


## INSTALLATION:
Adjust the install_path in the following code snipet and copy and paste it into your terminal.

```shell
# ENVIRONMENT
conda create -p D:\AI\env python=3.10.11 pytorch torchvision torchaudio cuda-python pytorch-cuda=11.8 -c pytorch -c nvidia -y
conda activate D:\AI\env

#Obsolete
#conda create -p D:\AI\env python=3.10.11
#pip install torch -f https://download.pytorch.org/whl/torch_stable.html
#conda install -c nvidia cuda-python=11.8

# LLM
conda install -c "nvidia/label/cuda-12.2.2" cuda-toolkit
pip install llama-cpp-python --prefer-binary --extra-index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu118
pip install numpy==1.22 --force

# TTS
# CUDA Toolkit: https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local
pip install TTS

# STT
pip install git+https://github.com/openai/whisper.git
pip install pyaudio sounddevice soundfile
choco install ffmpeg

# COMMANDS
pip install pygetwindow pywin32 pyautogui keyboard

# THERE IS A PROBLEM IN THE TTS PACKAGE. THE FOLLOWING NEEEDS TO BE CHANGED FOR THIS TO WORK:
# replace inside env\lib\site-packages\TTS\api.py the code line 109:
# with the following line:
# if self.model_name is not None and "xtts" in self.model_name:
```

*Models I used for testing:*

LLM:
- https://huggingface.co/TheBloke/Starling-LM-7B-alpha-GGUF/blob/main/starling-lm-7b-alpha.Q4_K_M.gguf
- https://huggingface.co/TheBloke/Starling-LM-7B-alpha-GGUF/blob/main/config.json

SA:
- https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest/tree/main

STT:
- whisper (small) (should download automatically once started)

TTS:
- tts_models--en--jenny--jenny (should download automatically once started)

## If you enjoy what I make, consider buying me a coffee for all these sleepless nights coding away (:
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/danielbenew)

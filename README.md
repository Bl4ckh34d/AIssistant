# AIssistant

A LLM assistant for personal computers that can open and close programs, tabs, folders and hold conversation via STT and TTS.
- Rudimentary Mood System: User and LLMs messages are put through sentiment analysis and rated positive or negative, influencing the AIs mood (BARELY TESTED)
- Rudimentary Longterm-Memory: Based on past chat logs, the LLM fills its context with chats older than 5 days, chats within the last 5 days and the most recent conversation. (UNTESTED)
- Shortterm-Memory should clean itself before reaching the token maximum

## NOTICE:
- I created this for myself in a private capacity and not for commercial use. It is not well tested, nor professionally built and the model prompt is TOXIC!
- This is WIP and might not work as expected.
- Adjust the paths in [commands.py](https://github.com/Bl4ckh34d/AIssistant/blob/5f7ef44548ab6323a588dc9b6d2560adafca794d/scripts/commands.py#L13-L30) to your needs. This script as well as [commands_list.py](https://github.com/Bl4ckh34d/AIssistant/blob/main/scripts/command_list.py) are interesting for you, if you want to add your own functionality. Saving and deleting files is currently not implemented for safety reasons. Also a more fine-grained control still needs to be worked out to give multiple commands in a single sentence.
- Also note, that not the answer of the LLM is responsible for triggering functions and tasks on the users machine. The users transcribed voice input is used for this. This way it is more reliable to trigger functions and also faster than waiting for the LLM to get it right.

## USAGE:
First you might want to adjust the paths to your programs and some other things inside [variables.py](https://github.com/Bl4ckh34d/AIssistant/blob/ac081c086708e21e9cc5ef2cf7832181d124d44b/scripts/variables.py#L75-L78).

```Start AIssistant.bat```

Enjoy talking to your very own AI Assistant. Tell the AI to open Firefox, close the tab or maximize the window, etc.
Start your commands with **"I command you..."**

#### **Currently implemented voice commands to trigger actions:**
- **AGAIN**: The word 'again' in a sentence without any of the other keywords will trigger the last action once more.)
- **GO BACK...** followed by **...TAB**: This should switch back by one tab
- **SCROLL...** followed by **...UP**: This should scroll the current active window up a fair bit.
- **SCROLL...** followed by **...DOWN**: This should scroll the current active window down a fair bit.
- **GO TO...**: This followed by a process name or folder should bring that folder/process to the foreground if it is currently open.
- **OPEN...**: This followed by a program or '...new folder at (Folder Location) should open the programm or folder at said location.
- **...NEW FOLDER TAB AT (FOLDER LOCATION)**: Opens a new tab in the currently active folder at the requested folder location
- **...NEW TAB**: Opens a new browser or program tab
- **CLOSE...** followed by **...WINDOW/TAB/etc.**: This Should close the requested window, tab or process
- **SWITCH...** followed by **...WINDOW/TAB**: Equivalent to pressing ALT + Tab
- **MINIMIZE...**: Minimizes active window
- **MAXIMIZE...**: Maximizes active window
- **REFRESH...**: Same as hitting F5 on the keyboard

#### **FOLDER LOCATIONS**:
C Drive, D Drive, AppData, Programs, Programs86, Home, Downloads

#### **CURRENTLY SUPPORTED PROGRAMS**:
Firefox, Firefox (Incognito), Explorer, VLC, Media Player Classic, Keepass, Steam, Discord, MS Word, MS Excel, MS Powerpoint, Notepad++,
VSC, PureRef, Audacity, Blender, Stable Diffusion, Calculator, System Settings

## REQUIREMENTS:
Pytorch:
- https://pytorch.org/get-started/locally/ is where you can find the current version of pytorch

Miniconda:
- https://docs.conda.io/projects/miniconda/en/latest/ is where you can find the current version of conda. THIS IS REQUIRED for the following install script. Paths also need to be adapted for your environment.


## INSTALLATION:
- Open a Windows Terminal and navigate to the folder where you want to install the AIssistant (*cd path/of/directory*).
- Adjust the install path (here D:) in the following lines of code where applicable and copy all the uncommented lines (without # in front) one by one into your terminal and hit enter after each line. If prompted to install/create files, confirm with yes (y).
- TTS currently causes an error, which is why you will have to add one line of code to the api.py script as described below.
- Download the **Large Language Model** (currently **only GGUF** supported) as well as the **Sentiment Analysis Model** and place them in the respective directory under models:
  -> The model and config file (**LLM**) need to be inside a folder with matching name of the model
  (ex. *./models/llm/starling-lm-7b-alpha.Q4_K_M/starling-lm-7b-alpha.Q4_K_M.gguf*).
  -> The following files from the Sentiment Analysis Model need to be placed into
  *./models/sa/cardiffnlp--twitter-roberta-base-sentiment-latest/cardiffnlp--twitter-roberta-base-sentiment-latest/pytorch_model.bin*:
    - config.json
    - pytorch_model.bin
    - special_tokens_map.json
    - tf_model.h5
    - vocab.json

See below for the links to these models.

```shell
# ENVIRONMENT
d:
git clone https://github.com/Bl4ckh34d/AIssistant.git
conda create -p D:\AIssistant\env python=3.10.11 pytorch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 cuda-python pytorch-cuda=12.1 -c pytorch -c nvidia
conda activate D:\AIssistant\env

# LLM
conda install -c "nvidia/label/cuda-12.2.2" cuda-toolkit
pip install https://github.com/jllllll/llama-cpp-python-cuBLAS-wheels/releases/download/wheels/llama_cpp_python-0.2.24+cu121-cp310-cp310-win_amd64.whl
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
# Inside \env\lib\site-packages\TTS\api.py insert the following line before 226:
if self.model_name is not None and "xtts" in self.model_name:
# and indent the following if-statements.
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

## TODO:
- Sentiment Score of LLM seems to not work as expected, need to revisit
- Browser extensions (Chrome and Firefox) for remote control through LLM
- Implement Youtube API / Google API / ChatGPT API
- Possibly integrate Open Interpreter and ditch my own code execution completely at some point, if OI integrates well into this.
- Since I don't use LangChain but rather built my own Longterm Memory System, I still need to implement the following things:
  - Once a json-Log is finished (current date =/= log date), and thie file is selected randomly to be in the memory, the LLM should add a summary of the conversation to the file. (skip this step if the summary is already in the file).
- Writing a scraper for search engines, wikipedia, weather forecast, etc. or giving the LLM API access to services for current information.
- Getting a embedding model (maybe sentence-transformers/all-MiniLM-L6-v2) to process outside information from Vector Index (pinecone-like but locally?) + embedding dataset

## If you enjoy what I make, consider buying me a coffee (:
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/danielbenew)

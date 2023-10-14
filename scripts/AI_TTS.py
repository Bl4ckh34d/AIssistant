import os, threading, contextlib, io
import soundfile as sf, variables as vars, helpers as help
from TTS.api import TTS
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

def invoke_text_to_speech(message):
    if message == "" or message == " ":
        print(Fore.RED + "PROBLEM: Nothing sent to TTS..." + Style.RESET_ALL)
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            text_to_speech(message)

def text_to_speech(message):
    tts = TTS(model_path=vars.tts_model_file_path, config_path=vars.tts_model_config_file_path, progress_bar=False).to("cuda")
    os.environ["TOKENIZERS_PARALLELISM"] = "True"
    tts.tts_to_file(text=message, file_path=vars.tts_output_file_path, gpu=True)
    
    # Play the wav file through the CABLE Input (VB-Audio Virtual C) device (ID 8)
    data, fs = sf.read(vars.tts_output_file_path)

    # Create threads for playing audio on respective devices
    thread_speakers = threading.Thread(target=help.play_audio, args=(data, fs, vars.AUDIO_DEVICE_ID_SPEAKERS))
    thread_virtual = threading.Thread(target=help.play_audio, args=(data, fs, vars.AUDIO_DEVICE_ID_VIRTUAL))

    # Start both threads
    thread_speakers.start()
    thread_virtual.start()

    # Wait for both threads to finish
    thread_speakers.join()
    thread_virtual.join()
import os
import soundfile as sf
from TTS.api import TTS
import torch
import threading
import helpers
import contextlib
import io
import variables as vars

def invoke_text_to_speech(message):
    if message == "" or message == " ":
        print("PROBLEM: Nothing sent to TTS...")
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            text_to_speech(message)

def text_to_speech(message):
    tts = TTS(model_path=r"D:\AI\models\tts\tts_models--en--jenny--jenny\model.pth", config_path=r"D:\AI\models\tts\tts_models--en--jenny--jenny\config.json", progress_bar=False).to("cuda")
    os.environ["TOKENIZERS_PARALLELISM"] = "True"
    tts.tts_to_file(text=message, file_path=vars.tts_output_file_path, gpu=True)
    
    # Play the wav file through the CABLE Input (VB-Audio Virtual C) device (ID 8)
    data, fs = sf.read(vars.tts_output_file_path)

    # Create threads for playing audio on respective devices
    thread_speakers = threading.Thread(target=helpers.play_audio, args=(data, fs, vars.AUDIO_DEVICE_ID_SPEAKERS))
    thread_virtual = threading.Thread(target=helpers.play_audio, args=(data, fs, vars.AUDIO_DEVICE_ID_VIRTUAL))

    # Start both threads
    thread_speakers.start()
    thread_virtual.start()

    # Wait for both threads to finish
    thread_speakers.join()
    thread_virtual.join()
import os
import soundfile as sf
from TTS.api import TTS
import threading
import helpers
import contextlib
import io

def invoke_text_to_speech(message):
    if message == "" or message == " ":
        print("PROBLEM: Nothing sent to TTS...")
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            text_to_speech(message)

def text_to_speech(message):
    path_to_file = '../recording/audio/last_output.wav'
    model_name = 'tts_models/en/ljspeech/vits' #'vocoder_models--en--ljspeech--univnet'
    tts = TTS(model_name)

    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    tts.tts_to_file(text=message, file_path=path_to_file, gpu=True)
    
    # Play the wav file through the CABLE Input (VB-Audio Virtual C) device (ID 8)
    data, fs = sf.read(path_to_file)
    device_id_virtual = 8 #8
    device_id_speakers = 6 #6

    # Create threads for playing audio on respective devices
    thread_speakers = threading.Thread(target=helpers.play_audio, args=(data, fs, device_id_speakers))
    thread_virtual = threading.Thread(target=helpers.play_audio, args=(data, fs, device_id_virtual))

    # Start both threads
    thread_speakers.start()
    thread_virtual.start()

    # Wait for both threads to finish
    thread_speakers.join()
    thread_virtual.join()
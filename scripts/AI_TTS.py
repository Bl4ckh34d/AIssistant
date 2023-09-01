import os
import sounddevice as sd
import soundfile as sf
from TTS.api import TTS
import threading

def play_audio(data, fs, device_id):
    print(f"Playing audio through device ID: {device_id}")
    sd.play(data, fs, device=device_id)
    sd.wait()

def text_to_speech(message):
    path_to_file = '../recording/audio/last_output.wav'
    model_name = 'tts_models/en/ljspeech/tacotron2-DDC' #'vocoder_models--en--ljspeech--univnet'
    tts = TTS(model_name)

    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    tts.tts_to_file(text=message, file_path=path_to_file, gpu=True)
    
    # Play the wav file through the CABLE Input (VB-Audio Virtual C) device (ID 8)
    data, fs = sf.read(path_to_file)
    device_id_virtual = 8 #8
    device_id_speakers = 6 #6

    # Create threads for playing audio on respective devices
    thread_speakers = threading.Thread(target=play_audio, args=(data, fs, device_id_speakers))
    thread_virtual = threading.Thread(target=play_audio, args=(data, fs, device_id_virtual))

    # Start both threads
    thread_speakers.start()
    thread_virtual.start()

    # Wait for both threads to finish
    thread_speakers.join()
    thread_virtual.join()
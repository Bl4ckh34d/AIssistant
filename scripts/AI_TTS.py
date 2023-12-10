import os, sys, threading, queue
import soundfile as sf, variables as vars, helpers as help
from TTS.api import TTS
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

# Initialize TTS
tts = TTS(model_path=vars.tts_model_file_path, config_path=vars.tts_model_config_file_path, progress_bar=False).to("cuda")
os.environ["TOKENIZERS_PARALLELISM"] = "True"

# Queue for managing playback
playback_queue = queue.Queue()
playback_lock = threading.Lock()  # Lock for synchronization

def play_audio_from_queue():
    while True:
        audio_file = playback_queue.get()
        data, fs = sf.read(audio_file)
        
        with playback_lock:  # Acquire the lock
            help.play_audio(data, fs)
            os.remove(audio_file)
            playback_queue.task_done()

def invoke_text_to_speech(message):
    # Start the playback thread
    playback_thread = threading.Thread(target=play_audio_from_queue)
    playback_thread.daemon = True
    playback_thread.start()

    sentence_array = help.split_reply_to_chunks(message)

    for index, sentence in enumerate(sentence_array, start=1):
        # Create Audio file
        file_path = f"{vars.tts_output_file_path}{index}.wav"
        # Redirect stdout to null device
        if not vars.verbose_tts:
            sys.stdout = open(os.devnull, 'w')
        tts.tts_to_file(text=sentence, file_path=file_path, gpu=True)
        # Reset stdout to default
        if not vars.verbose_tts:
            sys.stdout = sys.__stdout__
        playback_queue.put(file_path)  # Add file to the playback queue

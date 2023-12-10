import os, threading, contextlib, io, queue, time
import soundfile as sf, variables as vars, helpers as help
from TTS.api import TTS
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

def invoke_text_to_speech(message):
    if message == "" or message == " ":
        print(Fore.RED + "ERROR: Nothing sent to TTS..." + Style.RESET_ALL)
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            text_to_speech(message)

def text_to_speech(message):
    tts = TTS(model_path=vars.tts_model_file_path, config_path=vars.tts_model_config_file_path, progress_bar=False).to("cuda")
    os.environ["TOKENIZERS_PARALLELISM"] = "True"
    
    sentence_array = help.split_reply_to_chunks(message)
    
    for index, sentence in enumerate(sentence_array, start=1):
        # Create Audio file
        file_path = f"{vars.tts_output_file_path}{index}.wav"
        tts.tts_to_file(text=sentence, file_path=file_path, gpu=True)
        
        data, fs = sf.read(file_path)
        
        # Create threads for playing audio on respective devices
        thread_speakers = threading.Thread(target=help.play_audio, args=(data, fs))
        
        # Start both threads
        time.sleep(0.2)
        thread_speakers.start()
        
        # Wait for both threads to finish
        thread_speakers.join()

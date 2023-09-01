import whisper
import datetime
import requests
import os
import TTS
import contextlib
import io
import LLM

# GLOBAL VARIABLES
whisper_model = whisper.load_model("small") #tiny, base, small
language = "en"
task = "transcribe" #translate
current_dir = os.path.dirname(os.path.abspath(__file__))
audio_output_dir = os.path.join(current_dir, '../recording/audio')
audio_file_path = os.path.abspath(os.path.join(audio_output_dir, "last_input.wav"))
text_output_dir = os.path.join(current_dir, '../recording/text')

def transcribe_audio():
    global audio_output_dir
    global language
    global task
    
    print("> Transcribing...                                                          \
    ", end="\r", flush=True)
    
    # RECEIVING TRANSCRIPTION
    segments = whisper_model.transcribe(audio_file_path, language=language, task=task)
    
    # CLEANING UP TRANSCRIPTION
    transcription = ''.join(segments["text"])
    cleaned_transcription = transcription.strip() 
    
    # APPENDING MESSAGE TO HISTORY IN THE FORMAT OF Speaker:Message
    LLM.send_request(cleaned_transcription)
            
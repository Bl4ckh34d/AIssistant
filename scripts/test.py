import AI_LLM
import variables as vars
import commands as cmd
import helpers
import os
import whisper


# STT VARS
stt_model = whisper.load_model("small") #tiny, base, small
stt_model_language = "en"
stt_model_task = "transcribe" #translate
# PATHS
directory_current = os.path.dirname(os.path.abspath(__file__))
directory_audio = os.path.join(directory_current, '../recording/audio')
path_audio_input_file = os.path.abspath(os.path.join(directory_audio, "last_input.wav"))
path_audio_output_file = os.path.abspath(os.path.join(directory_audio, "last_output.wav"))
    
print("> Transcribing...                                                          \
", end="\r", flush=True)

# RECEIVING TRANSCRIPTION
segments = stt_model.transcribe(path_audio_input_file, language=stt_model_language, task=stt_model_task)

# CLEANING UP TRANSCRIPTION
transcription = ''.join(segments["text"])
cleaned_transcription = transcription.strip() 

print(cleaned_transcription)
            
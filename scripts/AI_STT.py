import AI_LLM
import variables as vars

def transcribe_audio():
    global audio_output_dir
    global language
    global task
    
    print("> Transcribing...                                                          \
    ", end="\r", flush=True)
    
    # RECEIVING TRANSCRIPTION
    segments = vars.whisper_model.transcribe(vars.audio_file_path, language=vars.language, task=vars.task)
    
    # CLEANING UP TRANSCRIPTION
    transcription = ''.join(segments["text"])
    cleaned_transcription = transcription.strip() 
    
    # APPENDING MESSAGE TO HISTORY IN THE FORMAT OF Speaker:Message
    AI_LLM.infer(cleaned_transcription)
            
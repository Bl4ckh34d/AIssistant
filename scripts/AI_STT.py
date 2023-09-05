import AI_LLM
import variables as vars

def transcribe_audio():
    
    print("> Transcribing...                                                          \
    ", end="\r", flush=True)
    
    # RECEIVING TRANSCRIPTION
    segments = vars.stt_model.transcribe(vars.path_audio_input_file, language=vars.stt_model_language, task=vars.stt_model_task)
    
    # CLEANING UP TRANSCRIPTION
    transcription = ''.join(segments["text"])
    cleaned_transcription = transcription.strip() 
    
    # APPENDING MESSAGE TO HISTORY IN THE FORMAT OF Speaker:Message
    AI_LLM.infer(cleaned_transcription)
            
import AI_LLM
import variables as vars
import commands as cmd
import helpers


def transcribe_audio():
    
    print("> Transcribing...                                                          \
    ", end="\r", flush=True)
    
    # RECEIVING TRANSCRIPTION
    segments = vars.stt_model.transcribe(vars.stt_input_file_path, language=vars.stt_model_language, task=vars.stt_model_task)
    
    # CLEANING UP TRANSCRIPTION
    transcription = ''.join(segments["text"])
    cleaned_transcription = transcription.strip() 
    
    # SENTIMENT ANALYSIS
    helpers.sentiment_calculation(cleaned_transcription)
    
    # CHECK FOR USER COMMANDS
    cmd.check_for_command(cleaned_transcription)
    AI_LLM.infer(cleaned_transcription)
            
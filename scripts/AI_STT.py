import AI_LLM
import variables as vars, commands as cmd, helpers as help


def transcribe_audio():
    
    print("> Transcribing...                                                          \
    ", end="\r", flush=True)
    
    # RECEIVING TRANSCRIPTION
    segments = vars.stt_model.transcribe(vars.stt_input_file_path, language=vars.stt_model_language, task=vars.stt_model_task)
    
    # CLEANING UP TRANSCRIPTION
    transcription = ''.join(segments["text"])
    cleaned_transcription = transcription.strip() 
    
    # SENTIMENT ANALYSIS
    help.sentiment_calculation(cleaned_transcription)
    
    # CHECK FOR USER COMMANDS
    if cmd.check_for_command(cleaned_transcription) == False:
        AI_LLM.infer(cleaned_transcription, help.get_current_time())
    else:
        AI_LLM.write_to_current_chat_history(vars.user_name, cleaned_transcription)
        AI_LLM.print_to_console(vars.user_name, cleaned_transcription, help.get_current_time())
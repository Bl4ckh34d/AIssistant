import AI_LLM, AI_TTS
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
    if cmd.check_for_command(cleaned_transcription) == []:
        AI_LLM.infer(cleaned_transcription)
    else:
        AI_LLM.write_to_history(vars.user_name, cleaned_transcription)
        AI_LLM.print_to_console(vars.user_name, cleaned_transcription)
        #AI_LLM.write_to_history(vars.ai_name, "Okay, done.")
        #AI_LLM.print_to_console(vars.ai_name, "Okay, done.")
        #AI_TTS.invoke_text_to_speech("Okay, done.")
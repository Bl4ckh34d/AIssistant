import recorder
import AI_LLM
import AI_TTS
import helpers

helpers.show_intro() 

input("Press Enter to continue...")
print()

AI_LLM.write_conversation(f"{AI_LLM.ai_name}", f"Alright, what do you need, {AI_LLM.user_name}?")
AI_TTS.invoke_text_to_speech(f"Alright, what do you need, {AI_LLM.user_name}?")

recording = recorder.Recorder()
recording.listen()
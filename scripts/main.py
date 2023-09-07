import recorder
import AI_LLM
import AI_TTS
import helpers
import variables as vars

helpers.show_intro()

print()
input("Press Enter to continue...")
print()

AI_LLM.write_conversation(f"{vars.ai_name}", f"Alright, what do you need?")
AI_TTS.invoke_text_to_speech(f"Alright, what do you need?")

recording = recorder.Recorder()
recording.listen()
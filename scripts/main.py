import recorder, AI_LLM
import helpers as help, variables as vars

help.show_intro()
help.build_memory()

print()
input(f"Press Enter to wake {vars.ai_name}...")
print()

AI_LLM.infer("")

recording = recorder.Recorder()
recording.listen()
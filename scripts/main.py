import recorder, AI_LLM
import helpers as help, variables as vars

help.show_intro()
help.build_memory()

print()
input("Press Enter to continue...")
print()

AI_LLM.infer("")

recording = recorder.Recorder()
recording.listen()
import recorder, AI_LLM
import helpers as help, variables as vars

help.show_intro()
help.build_memory()

print()
name = input(f"Enter your name: ")
if name is not "" and name is not " ":
    vars.user_name = name
print()

AI_LLM.infer("")

recording = recorder.Recorder()
recording.listen()
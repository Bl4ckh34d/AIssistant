import recorder, AI_LLM, subprocess
import helpers as help, variables as vars

subprocess.call('cls', shell=True)
help.show_intro()
help.build_memory()

print()
name = input(f"Enter your name: ")
if name != "" and name != " ":
    vars.user_name = name
print()

AI_LLM.infer("")

recording = recorder.Recorder()
recording.listen()
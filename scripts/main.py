import recorder
import helpers
import AI_LLM

helpers.show_intro()
helpers.build_memory()

print()
input("Press Enter to continue...")
print()

AI_LLM.infer2("")
#AI_LLM.infer("")

recording = recorder.Recorder()
recording.listen()
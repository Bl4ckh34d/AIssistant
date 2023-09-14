import recorder
import helpers

helpers.show_intro()
helpers.build_memory()

print()
input("Press Enter to continue...")
print()

recording = recorder.Recorder()
recording.listen()
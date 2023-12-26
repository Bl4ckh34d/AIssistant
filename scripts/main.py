import recorder
import helpers as help

help.setup_user_name()
help.setup_user_gender()
help.setup_ai_name()
help.setup_ai_gender()
help.setup_audio_input()
help.setup_audio_output()
help.show_instructions()
help.build_memory()

recording = recorder.Recorder()
recording.listen()
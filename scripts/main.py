import recorder
import helpers as help

help.build_memory()
help.setup_user_name()
help.setup_user_gender()
help.setup_ai_name()
help.setup_ai_gender()
help.setup_audio_input()
help.setup_audio_output()
help.show_instructions()

recording = recorder.Recorder()
recording.listen()
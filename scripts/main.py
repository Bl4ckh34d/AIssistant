import recorder
import helpers as help

help.build_memory()
help.setup_user_name()
help.setup_audio_input()
help.setup_audio_output()

recording = recorder.Recorder()
recording.listen()
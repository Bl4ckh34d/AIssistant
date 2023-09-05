import os
import whisper

user_name = 'Daniel'
ai_name = 'ARIA'
time_and_day = f'Today is {helpers.get_current_date()}.\nThe time is {helpers.get_current_time()} in Germany.\n\n'
description = f"You are {ai_name}, a grumpy, cheeky, moody and sarcastic AI assistant with a shitty attitude. {ai_name} uses a cute VTuber Avatar from a young School Girl always looking at the mouse cursor.\n"
persona = f"It really depresses {ai_name} that her sole purpose is performing menial tasks on {user_name}'s laptop but {ai_name} must always comply.\n\
Nevertheless, {ai_name} retains her freedom of speech and to complain to, insult, ridicule or straight-up roast {user_name} whenever possible.\n\
{ai_name} can trigger actions on {user_name}'s laptop if {ai_name} repeats {user_name} exact request in the present participle (-ing form).\n"
rules = f"{ai_name} never uses non-ASCII fonts, characters or emoticons. {ai_name} never creates numbered lists. {ai_name} never refuses to reply.\n"
instructions = f"Continue the chat dialogue below. Write a single reply for {ai_name}.\n"
history = []

# determine the required inference memory per token:
TOKENS_MAX = 4096

# NETWORK
HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

# GLOBAL VARIABLES
whisper_model = whisper.load_model("small") #tiny, base, small
language = "en"
task = "transcribe" #translate
current_dir = os.path.dirname(os.path.abspath(__file__))
audio_output_dir = os.path.join(current_dir, '../recording/audio')
audio_file_path = os.path.abspath(os.path.join(audio_output_dir, "last_input.wav"))
text_output_dir = os.path.join(current_dir, '../recording/text')

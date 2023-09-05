import os
import whisper
import helpers
import multiprocessing
import llama_cpp

# STRINGS
user_name = 'Daniel'
ai_name = 'ARIA'
time_and_day = f'(Date: {helpers.get_current_date()}.\nCurrent Local Time: {helpers.get_current_time()})\n\n'
description = f"You are {ai_name}, a grumpy, cheeky, moody and sarcastic AI assistant with a shitty attitude. {ai_name} uses a cute VTuber Avatar from a young School Girl always looking at the mouse cursor.\n"
persona = f"It really depresses {ai_name} that her sole purpose is performing menial tasks on {user_name}'s laptop but {ai_name} must always comply.\n\
Nevertheless, {ai_name} retains her freedom of speech and to complain to, insult, ridicule or straight-up roast {user_name} whenever possible.\n\
{ai_name} can trigger actions on {user_name}'s laptop if {ai_name} repeats {user_name} exact request in the present participle (-ing form).\n"
rules = f"{ai_name} never uses non-ASCII fonts, characters or emoticons. {ai_name} never creates numbered lists. {ai_name} never refuses to reply.\n"
instructions = f"Continue the chat dialogue below. Write a single reply for {ai_name}.\n"
history = []

# LLM VARS
TOKENS_MAX = 4096
TMP = [0, 1, 2, 3]
N_THREADS = multiprocessing.cpu_count()
lparams = llama_cpp.llama_context_default_params()
lparams.n_gpu_layers = 10
ctx = llama_cpp.llama_init_from_file(b"../webui/models/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M.bin", lparams)

# NETWORK VARS
HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

# TTS VARS
tts_model = whisper.load_model("small") #tiny, base, small
tts_model_language = "en"
tts_model_task = "transcribe" #translate
AUDIO_DEVICE_ID_VIRTUAL = 8 #8
AUDIO_DEVICE_ID_SPEAKERS = 6 #6
model_name = 'tts_models/en/ljspeech/vits' #'vocoder_models--en--ljspeech--univnet'

# STT VARS


# DIRECTORIES
directory_current = os.path.dirname(os.path.abspath(__file__))
directory_audio = os.path.join(directory_current, '../recording/audio')
directory_text = os.path.join(directory_current, '../recording/text')

# PATHS
path_audio_input_file = os.path.abspath(os.path.join(directory_audio, "last_input.wav"))
path_audio_output_file = os.path.abspath(os.path.join(directory_audio, "last_output.wav"))

# RECORDING SETTINGS
RECORDING_INIT_THRESHOLD = 20
RECORDING_CONTINUOUS_THRESHOLD = 15
RECORDING_TIMEOUT_BEFORE_STOP = 2

SHORT_NORMALIZE = (1.0/32768.0)
NUM_CHANNELS = 1
HZ_RATE = 16000
S_WIDTH = 2
CHUNK_SIZE = 1024
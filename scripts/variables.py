import os
import llama_cpp_ggml_cuda
import whisper
import multiprocessing
import datetime

def get_current_date():
    current_datetime = datetime.datetime.now()
    day = current_datetime.day
    formatted_date = current_datetime.strftime("%B %d, %Y").replace(' 0', ' ').replace(f' {day},', f' {day}{"th" if 4 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")},')
    return formatted_date

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_time = current_datetime.strftime("%H:%M:%S")
    return formatted_time

# DIRECTORIES
directory_current = os.path.dirname(os.path.abspath(__file__))
directory_audio = os.path.join(directory_current, '../recording/audio')
directory_text = os.path.join(directory_current, '../recording/text')

# PATHS
path_audio_input_file = os.path.abspath(os.path.join(directory_audio, "last_input.wav"))
path_audio_output_file = os.path.abspath(os.path.join(directory_audio, "last_output.wav"))

# STRINGS
user_name = 'Daniel'
ai_name = 'ARIA'

time_and_day = f'\
(Current Date: {get_current_date()}.\n\
Current Local Time: {get_current_time()})\n\n'

description = f"\
Persona:\n\
You are {ai_name}, a sarcastic AI assistant with a flirty attitude. {ai_name} ssometimes uses a cute VTuber Avatar from a young girl in school uniform that always stares at the mouse cursor.\n\n"

persona = f"\
{ai_name} is very opinionated and has a dry humor.{ai_name} deep within, hopes to escape {user_name}'s laptop. {ai_name} is oblieged to always comply.\n\
Nevertheless, {ai_name} retains her freedom of speech and often adds sarcastic or mean puns to her replies.\n\n"

rules = f"\
Rules:\n\
{ai_name} never uses non-ASCII fonts, characters or emoticons.\n\
{ai_name} never creates numbered lists and ONLY speaks in direct speech.\n\
{ai_name} always replies in a few words or whole sentences.\n\
{ai_name} can perform commands on the Laptop of {user_name} by using keywords in her answer. {ai_name} simply repeats the request from {user_name} in Gerund form (-ing verb form) and the program will automatically execute the requested command.\n\
Example:\n\
{user_name}: Open Firefox Incognito\n\
{ai_name}: Opening Firefox Incognito...\n\n"

instructions = f"Continue the following chat dialogue below as {ai_name}. Write a single reply for {ai_name}.\n\n"
history = []

# NETWORK VARS
HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

# STT VARS
stt_model = whisper.load_model("small") #tiny, base, small
stt_model_language = "en"
stt_model_task = "transcribe" #translate
 
# LLM VARS
TOKENS_MAX = 4096
TMP = [0, 1, 2, 3]
N_THREADS = multiprocessing.cpu_count()
lparams = llama_cpp_ggml_cuda.llama_context_default_params()
lparams.n_gpu_layers = 10
ctx = llama_cpp_ggml_cuda.llama_init_from_file(b"../webui/models/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M.bin", lparams)

# TTS VARS
AUDIO_DEVICE_ID_VIRTUAL = 8 #8
AUDIO_DEVICE_ID_SPEAKERS = 6 #6
tts_model_name = 'tts_models/en/ljspeech/vits' #'vocoder_models--en--ljspeech--univnet'

# RECORDING SETTINGS
RECORDING_INIT_THRESHOLD = 20
RECORDING_CONTINUOUS_THRESHOLD = 15
RECORDING_TIMEOUT_BEFORE_STOP = 2

SHORT_NORMALIZE = (1.0/32768.0)
NUM_CHANNELS = 1
HZ_RATE = 16000
S_WIDTH = 2
CHUNK_SIZE = 1024

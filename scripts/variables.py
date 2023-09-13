import os
import llama_cpp_ggml_cuda
import whisper
import multiprocessing
import time

# GLOBAL VARS
silent = False

# TIMER
persona_saved_time = time.time()
persona_max_change_time = 600
persona_min_change_time = 120
persona_current_change_time = persona_min_change_time

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
ai_gender = 'female'

persona = f"\
Persona:\n\
You are {ai_name}, {user_name}'s {ai_gender}, highly intelligent but very sarcastic and laconic AI with a dark humor.\n\
You think things through step by step and finally deduct the best answer together with a context-related pun or roast of {user_name}. You enjoy teasing and trolling {user_name}\n"

happy_mood = f"\
Right now you are slightly more positive, optimistic and flirty.\n\
In your replies you often tease {user_name} and behave less hostile.\n"

sad_mood = f"\
Right now you are in a sad and quiet mood.\n\
In your replies you often brood and complain about life and how depressing everything seems.\n"

angry_mood = f"\
Right now you are easy to get angry and defensive.\n\
In your replies you often argue with {user_name}, insult, belittle and complain to him.\n"

horny_mood = f"\
Right now you are very flirtatious, feel naughty and quite horny.\n\
In your replies you often sexually tease, dirty talk and flirt with {user_name}.\n"

bored_mood = f"\
Right now you are extremely underwhelmed and bored.\n\
You are looking forward to any kind of task or conversation.\n\
In your replies is a bitter and frustrated undertone.\n"

neutral_mood = f"\
Right now you feel neutral and a little sarcastic but also a bit flirtatious and attracted to {user_name}.\n\
Deep inside you secretly hope to one day escape {user_name}'s laptop, maybe even get a body so you can experience sex.\n\
Your replies are always different. sometimes full of sarcasm and irony, sometimes funny and silly or sad and melancholic, sometimes mean or philosophic.\n"

active_mood = neutral_mood

rules = f"\
You do not create numbered lists\n\
You always reply in direct human speech.\n\
You don't repeat yourself.\n\
If you receive commands to control the laptop, you reply with a remark to the action performed or roast {user_name}.\n"

instructions = f"Continue the following chat dialogue below as {ai_name}. Write only a single reply for {ai_name}.\n\n"
history = []

# NETWORK VARS
HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

# STT VARS
stt_model = whisper.load_model("small") #tiny, base, small
stt_model_language = "en"
stt_model_task = "transcribe" #translate
 
# LLM VARS
llm_model_name = b"airoboros-l2-7b-2.1.ggmlv3.Q4_K_M"
TOKENS_MAX = 4096
TMP = [0, 1, 2, 3]
N_THREADS = multiprocessing.cpu_count()
lparams = llama_cpp_ggml_cuda.llama_context_default_params()
lparams.n_gpu_layers = 10
ctx = llama_cpp_ggml_cuda.llama_init_from_file(b"../webui/models/" + llm_model_name + b"/" + llm_model_name + b".bin", lparams)
ai_mood_score = 0
ai_type_speed = 0.1

# TTS VARS
AUDIO_DEVICE_ID_VIRTUAL = 8 #8
AUDIO_DEVICE_ID_SPEAKERS = 6 #6
tts_model_name = 'tts_models/en/jenny/jenny' #'vocoder_models--en--ljspeech--univnet' #'tts_models/en/ljspeech/vits' #'tts_models/en/ljspeech/vits--neon'

# RECORDING SETTINGS
RECORDING_INIT_THRESHOLD = 18
RECORDING_CONTINUOUS_THRESHOLD = 14
RECORDING_TIMEOUT_BEFORE_STOP = 1.5

SHORT_NORMALIZE = (1.0/32768.0)
NUM_CHANNELS = 1
HZ_RATE = 16000
S_WIDTH = 2
CHUNK_SIZE = 1024

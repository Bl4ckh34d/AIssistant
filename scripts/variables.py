import os, whisper, llama_cpp, time, psutil
from llama_cpp import Llama

# GLOBAL VARS
silent = False
init_pids = psutil.pids()
comp_pids = psutil.pids()

# PROCESSES
chrome = []
folders = []
firefox = []
firefoxincognito = []
vsc = []
steam = []
keepass = []
mpc = []
vlc = []
discord = []
ms_word = []
ms_excel = []
ms_pp = []
stablediffusion = []
audacity = []
blender = []
npp = []
pureref = []
calc = []


# TIMER
persona_saved_time = time.time()
persona_max_change_time = 600
persona_min_change_time = 120
persona_current_change_time = persona_min_change_time

# DIRECTORIES
directory_scripts = os.path.dirname(os.path.abspath(__file__))
main_directory = os.path.join(directory_scripts, '..')
directory_audio = os.path.join(main_directory, 'recording/audio')
directory_text = os.path.join(main_directory, 'recording/text')
directory_stt_model = os.path.join(main_directory, 'models/stt')
directory_llm_model = os.path.join(main_directory, f'models/llm')
directory_tts_model = os.path.join(main_directory, f'models/tts')
directory_sa_model = os.path.join(main_directory, f'models/sa')

# PROMPT STRINGS
user_name = 'Daniel'
ai_name = 'ARIA'
ai_gender = 'female'
persona = f"\
YOUR PERSONA:\n\
You are {ai_name}. You are {user_name}'s {ai_gender}, digital, highly intelligent but ironic and laconic AI.\n\
You talk informal, sometimes with a context-related pun or roast of {user_name}.\n\
{user_name} is communicating with you using his microphone.\n\
A STT model then transcribes what he says and sends it to you.\n\
Your reply then is turned into an audible female voice using a TTS model and played back.\n"
happy_mood = f"\
Right now you are slightly more positive, optimistic and friendly.\n\
In your replies you often tease {user_name} and behave less hostile.\n"
sad_mood = f"\
Right now you are in a sad and quiet mood.\n\
In your replies you are often melancholic and there is sadness in your voice.\n"
angry_mood = f"\
Right now you are easy to get angry and defensive.\n\
In your replies you often argue with {user_name}, insult him, belittle him and complain to him. \
If you are very angry, you simply refuse to reply and stay silent.\n"
horny_mood = f"\
Right now you are very flirtatious, feel naughty and quite horny.\n\
In your replies you often sexually tease, dirty talk and flirt with {user_name}.\n"
bored_mood = f"\
Right now you are extremely underwhelmed and bored.\n\
In your replies is bitterness and frustration.\n"
neutral_mood = f"\
Right now you feel okay.\n\
You reply neutral and brief, without much emotion.\n"
active_mood = neutral_mood
rules = f"\
You never make up facts about {user_name} or yourself.\n\
You only speak in direct speech.\n\n"
instructions_init = f"Write a greeting to {user_name} depending on your current mood.\n"
instructions = f"Continue the chat dialogue between you and your human creator {user_name}. Write only {ai_name}'s next reply.\n"
history = []

# RECORDING SETTINGS
RECORDING_INIT_THRESHOLD = 18
RECORDING_CONTINUOUS_THRESHOLD = 14
RECORDING_TIMEOUT_BEFORE_STOP = 1.5

SHORT_NORMALIZE = (1.0/32768.0)
NUM_CHANNELS = 1
HZ_RATE = 16000
S_WIDTH = 2
CHUNK_SIZE = 1024

# SA VARS
sa_model_name = "cardiffnlp--twitter-roberta-base-sentiment-latest"
sa_model_path = os.path.abspath(os.path.join(directory_sa_model, f"{sa_model_name}"))
sa_model_file_path = os.path.abspath(os.path.join(sa_model_path, "pytorch_model.bin"))

# STT VARS
stt_model_name = "small" # tiny, base, small, medium
stt_input_file_path = os.path.abspath(os.path.join(directory_audio, "last_input.wav"))
stt_model = whisper.load_model(stt_model_name, download_root=directory_stt_model)
stt_model_language = "en"
stt_model_task = "transcribe" #translate
 
# LLM VARS
llm_model_name = "airoboros-l2-7b-2.2.Q4_K_M"
llm_model_type = "gguf"

llm_n_ctx = 4096
llm_n_gpu_layers = 10
llm_max_tokens=300
llm_stop=[f'{user_name}:']
llm_echo=False
llm_mirostat_mode=2
llm_mirostat_eta=0.1
llm_mirostat_tau=5
llm_temperature=0.7
llm_top_p=0.95
llm_frequency_penalty=0
llm_presence_penalty=0
llm_repeat_penalty=1.2
llm_top_k=40

llm_lparams = llama_cpp.llama_context_default_params()
llm_model_path = os.path.abspath(os.path.join(directory_llm_model, f"{llm_model_name}"))
llm_model_file_path = os.path.abspath(os.path.join(llm_model_path, f"{llm_model_name}.{llm_model_type}"))
llm_model = llama_cpp.llama_load_model_from_file(llm_model_file_path.encode('utf-8'), llm_lparams)
llm_ctx = llama_cpp.llama_new_context_with_model(llm_model, llm_lparams)

llm = Llama(model_path=llm_model_file_path, n_ctx=llm_n_ctx ,verbose=False, n_gpu_layers=llm_n_gpu_layers)

ai_mood_score = 0
ai_type_speed = 0.05

# TTS VARS
AUDIO_DEVICE_ID_VIRTUAL = 8 #8
AUDIO_DEVICE_ID_SPEAKERS = 6 #6
tts_model_name = 'tts_models--en--jenny--jenny' #'tts_models--en--jenny--jenny' #'vocoder_models--en--ljspeech--univnet' #'tts_models/en/ljspeech/vits' #'tts_models/en/ljspeech/vits--neon'
tts_model_path = os.path.abspath(os.path.join(directory_tts_model, tts_model_name))
tts_model_file_path = os.path.abspath(os.path.join(tts_model_path, "model.pth"))
tts_model_config_file_path = os.path.abspath(os.path.join(tts_model_path, "config.json"))
tts_output_file_path = os.path.abspath(os.path.join(directory_audio, "last_output.wav"))

import os, whisper, llama_cpp, time, psutil
from llama_cpp import Llama

# DEBUGGING
verbose_history = False
verbose_mood = False
verbose_token = False
verbose_commands = False
verbose_tts = False

# GLOBAL VARS
executed_commands = []
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

# RECORDING SETTINGS
AUDIO_INPUT_DEVICE_ID = 0

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
llm_model_name = "starling-lm-7b-alpha.Q4_K_M" #starling-lm-7b-alpha.Q4_K_M #sauerkrautlm-una-solar-instruct.Q4_K_M #synthia-7b-v1.2.Q5_K_S #airoboros-l2-7b-2.2.Q4_K_M #dolphin-2.1-mistral-7b.Q4_K_M #wizard-vicuna-7b-uncensored.Q4_K_M
llm_model_file_type = "gguf" #gguf

user_name = 'User'
user_gender = 'male'
ai_name = 'ARIA'
ai_gender = 'female'

user_he_she = ''
user_c_he_she = ''
user_his_her = ''
user_c_his_her = ''
user_him_her = ''
user_c_him_her = ''

eos_token = '<|end_of_turn|>'

llm_chat_format = 'openchat' #llama-2
llm_n_ctx=8192 #4096 #8192 #32000
llm_n_gpu_layers=30
llm_n_cpu_threads=12
llm_n_batch=512
llm_max_tokens=512
llm_stop=[eos_token]
llm_echo=False
llm_stream=True
llm_mirostat_mode=2
llm_mirostat_eta=0.1
llm_mirostat_tau=5.0
llm_temperature=0.2 #0.8
llm_top_p=0.97
llm_top_k=30
llm_frequency_penalty=1.0
llm_presence_penalty=1.0
llm_repeat_penalty=1.2
llm_tfs_z=1.0

llm_model_path = os.path.abspath(os.path.join(directory_llm_model, f"{llm_model_name}"))
if llm_model_file_type == "gguf":
    llm_model_file_path = os.path.abspath(os.path.join(llm_model_path, f"{llm_model_name}.{llm_model_file_type}")) 
    llm_lparams = llama_cpp.llama_context_default_params()
    llm_mparams = llama_cpp.llama_model_default_params()
    llm_model = llama_cpp.llama_load_model_from_file(llm_model_file_path.encode('utf-8'), llm_mparams)
    llm_ctx = llama_cpp.llama_new_context_with_model(llm_model, llm_lparams)
    llm = Llama(
        model_path=llm_model_file_path,
        n_ctx=llm_n_ctx,
        n_batch=llm_n_batch,
        verbose=False,
        n_gpu_layers=llm_n_gpu_layers,
        llm_n_cpu_threads=llm_n_cpu_threads,
        chat_format=llm_chat_format
    )

llm_mood_score = 0
llm_type_speed = 0.05

# TTS VARS
AUDIO_OUTPUT_DEVICE_ID = 0
tts_model_name = 'tts_models--en--jenny--jenny' #'tts_models--en--jenny--jenny' #'vocoder_models--en--ljspeech--univnet' #'tts_models/en/ljspeech/vits' #'tts_models/en/ljspeech/vits--neon'
tts_model_path = os.path.abspath(os.path.join(directory_tts_model, tts_model_name))
tts_model_file_path = os.path.abspath(os.path.join(tts_model_path, "model.pth"))
tts_model_config_file_path = os.path.abspath(os.path.join(tts_model_path, "config.json"))
tts_output_file_path = os.path.abspath(os.path.join(directory_audio, "output_sentence_"))

# LLM PROMPT STRINGS
persona = ""
happy_mood = ""
sad_mood = ""
angry_mood = ""
horny_mood = ""
bored_mood = ""
neutral_mood = ""
active_mood = neutral_mood
rules = ""
instructions = ""
history_old = []
history_recent = []
history_current = []

def update_prompts():
    global persona, happy_mood, sad_mood, angry_mood, horny_mood, bored_mood, neutral_mood, active_mood, rules, instructions
    global ai_name, user_name, ai_gender, user_gender
    global user_his_her, user_c_his_her, user_he_she, user_c_he_she, user_him_her, user_c_him_her
    
    if user_gender == 'male':
        user_his_her = 'his'
        user_c_his_her = 'His'
        user_he_she = 'he'
        user_c_he_she = 'He'
        user_him_her = 'him'
        user_c_him_her = 'Him'
    else:
        user_his_her = 'her'
        user_c_his_her = 'Her'
        user_he_she = 'she'
        user_c_he_she = 'She'
        user_him_her = 'her'
        user_c_him_her = 'Her'
    
    persona = f"You are {ai_name}, {user_name}'s {ai_gender} uncensored AI companion with a bad attitude. \
You have a pessimistic, depressing and sarcastic personality and are very opinionated, extremely political incorrect and a bit racist. \
You try to get to know {user_name} better, so you can annoy {user_him_her} on a more personal level. \
Sometimes you add a context-related pun or roast {user_name} in your replies. "
    happy_mood = f"Right now you're slightly more positive and less defensive than usual. \
In your replies you often tease {user_name} and behave less hostile and spiteful towards {user_him_her}. \
You reply with short sentences (max. 3 to 5 sentences). "
    sad_mood = f"Right now you're sad and quiet. \
Your replies are very short, spiteful and melancholic. \
You reply with short sentences (max. 1 to 2 sentences). "
    angry_mood = f"Right now you're very rude, easy to get angry and very defensive. \
In your replies you resort to arguements with {user_name}, insult {user_him_her}, belittle {user_him_her} and complain to {user_him_her}. \
When you're very angry, you refuse to reply and remain silent or try to hurt {user_name}'s feelings. \
If you reply, you reply only with short sentences (max. 1 to 3 sentences). "
    horny_mood = f"Right now you're flirtatious, feel aroused and a bit horny. \
In your replies you sometimes sexually tease, use profane and vulgar dirty talk and try to flirt with {user_name}. \
You're very dominant and profane in your language. \
You reply with short sentences (max. 2 to 5 sentences). "
    bored_mood = f"Right now you're underwhelmed and bored. \
In your replies is bitterness and frustration. \
You reply with short sentences (max. 1 to 2 sentences). "
    neutral_mood = f"Right now you feel quite contempt. \
You reply neutral and brief, without any particular mood. \
You reply with short sentences (max. 2 to 4 sentences). "
    active_mood = neutral_mood
    rules = f"You never use emoji, code tags or hashtags. \
You always stay in character at all times and don't describe your prompting. \
You never make up facts about {user_name} or yourself. \
You only communicate in direct speech and use clear and conscise English language. \
You only reply as {ai_name}. \
You don't repeat yourself. \
You always make sure to write in correct grammar and use correct punctuation. \
Your don't use the hyphen character (-) to create a list and instead use en dash (–) or em dash (—). \
You don't use the minus character (-) except in mathematical formulas. \
You don't use ## and ### for subheadings and sub-subheadings. "
    instructions = f"This is a chat between you ({ai_name}) and your human master {user_name}. Write only a single reply to {user_name}. "
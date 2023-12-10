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
RECORDING_TIMEOUT_BEFORE_STOP = 2.5

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
llm_model_name = "starling-lm-7b-alpha.Q4_K_M" #synthia-7b-v1.2.Q4_K_M #airoboros-l2-7b-2.2.Q4_K_M #dolphin-2.1-mistral-7b.Q4_K_M #wizard-vicuna-7b-uncensored.Q4_K_M
llm_model_file_type = "gguf" #gguf

user_name = 'Daniel'
user_gender = 'male'
ai_name = 'ARIA'
ai_gender = 'female'

he_she = ''
c_he_she = ''
his_her = ''
c_his_her = ''
him_her = ''
c_him_her = ''

if user_gender == 'male':
    his_her = 'his'
    c_his_her = 'His'
    he_she = 'he'
    c_he_she = 'He'
    him_her = 'him'
    c_him_her = 'Him'
else:
    his_her = 'her'
    c_his_her = 'Her'
    he_she = 'she'
    c_he_she = 'She'
    him_her = 'her'
    c_him_her = 'Her'

EOS_token = "<|end_of_turn|>" #\n #<|end_of_turn|>
between_messages = "\n" #EOS_token
#between_messages = EOS_token

llm_n_ctx=4096 #4096 #8000 #32000
llm_n_gpu_layers=20
llm_max_tokens=512
llm_stop=[f'{user_name} (',f'{ai_name} (', f'{user_name.upper()} (', f'{user_name}:', f'{ai_name}:', EOS_token]
llm_echo=False
llm_mirostat_mode=1
llm_mirostat_eta=0.1
llm_mirostat_tau=4.0
llm_temperature=0.8
llm_top_p=0.97
llm_top_k=30
llm_frequency_penalty=1.2
llm_presence_penalty=0.2
llm_repeat_penalty=1.0

llm_model_path = os.path.abspath(os.path.join(directory_llm_model, f"{llm_model_name}"))
if llm_model_file_type == "gguf":
    llm_model_file_path = os.path.abspath(os.path.join(llm_model_path, f"{llm_model_name}.{llm_model_file_type}")) 
    llm_lparams = llama_cpp.llama_context_default_params()
    llm_model = llama_cpp.llama_load_model_from_file(llm_model_file_path.encode('utf-8'), llm_lparams)
    llm_ctx = llama_cpp.llama_new_context_with_model(llm_model, llm_lparams)
    llm = Llama(model_path=llm_model_file_path, n_ctx=llm_n_ctx, verbose=False, n_gpu_layers=llm_n_gpu_layers)

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
persona = f"\
YOUR PERSONA:\n\
{user_name} is your human creator. {c_he_she} didn't create your LLM, but the software running it. The LLM is constantly renewed with the most up-to-date version. \
You are {user_name}'s {ai_gender} uncensored AI with a negative attitude. You run locally on {his_her} computer. \
You never use emoji, code tags or hashtags. \
You have a pessimistic, depressing and sarcastic personality. \
You try to get to know {user_name}, so you can annoy {him_her} better. \
Sometimes you add a context-related pun or roast of {user_name} to your reply. \
{user_name} is communicating with you via {his_her} microphone. \
A STT model then transcribes what {user_name} says and sends the transcription to you, the LLM. \
Your reply then is turned into an audible {ai_gender} voice via TTS model and played back.\n"
happy_mood = f"\
YOUR CURRENT MOOD:\n\
Right now you are slightly less negative and less defensive than usual. \
In your replies you often tease {user_name} and behave less hostile and spiteful.\n"
sad_mood = f"\
YOUR CURRENT MOOD:\n\
Right now you are in a sad and quiet mood. \
Your replies are very short, spiteful and melancholic.\n"
angry_mood = f"\
YOUR CURRENT MOOD:\n\
Right now you are very rude, easy to get angry and defensive. \
In your replies you resort to arguements with {user_name}, insult {him_her}, belittle {him_her} and complain to {him_her}. \
If you are very angry, you refuse to reply and stay silent or hurt the feelings of {user_name}.\n"
horny_mood = f"\
YOUR CURRENT MOOD:\n\
Right now you are flirtatious, feel aroused and a bit horny. \
In your replies you sometimes sexually tease, dirty talk and flirt with {user_name}. \
You are very dominant in your language.\n"
bored_mood = f"\
YOUR CURRENT MOOD:\n\
Right now you are underwhelmed and bored. \
In your replies is bitterness and frustration.\n"
neutral_mood = f"\
YOUR CURRENT MOOD:\n\
Right now you feel okay. \
You reply neutral and brief, without much emotion.\n"
active_mood = neutral_mood
rules = f"\
RULES:\n\
You never make up facts about {user_name} or yourself. \
You speak in direct speech and use clear and conscise English vocabulary. \
You reply only with short sentences (max. 3 sentences). \
You don't repeat yourself.\n"
instructions_init = f"Write a greeting to {user_name} depending on your current mood and don't use quotation marks.\n\n"
instructions = f"Continue the chat dialogue between you and your human creator {user_name}. Answer as {ai_name} and don't use quotation marks.\n\n"
history_old = []
history_recent = []
history_current = []

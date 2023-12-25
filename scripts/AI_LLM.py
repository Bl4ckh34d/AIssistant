import re, threading, queue, os, sys
import soundfile as sf, sounddevice as sd, variables as vars, helpers as help
from TTS.api import TTS
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

# Initialize TTS
tts = TTS(model_path=vars.tts_model_file_path, config_path=vars.tts_model_config_file_path, progress_bar=False).to("cuda")
os.environ["TOKENIZERS_PARALLELISM"] = "True"

# Queue for managing playback
playback_queue = queue.Queue()
playback_lock = threading.Lock()  # Lock for synchronization

def play_audio_from_queue():
    while True:
        audio_file = playback_queue.get()
        data, fs = sf.read(audio_file)
        
        with playback_lock:  # Acquire the lock
            sd.play(data, fs, device=vars.AUDIO_OUTPUT_DEVICE_ID)
            sd.wait()
            os.remove(audio_file)
            playback_queue.task_done()

def invoke_text_to_speech(message):
    sentence_array = help.split_reply_to_chunks(message)

    for index, sentence in enumerate(sentence_array, start=1):
        file_path = f"{vars.tts_output_file_path}{index}.wav"
        
        if not vars.verbose_tts:
            sys.stdout = open(os.devnull, 'w')
            
        tts.tts_to_file(text=sentence, language="en", file_path=file_path, gpu=True)

        if not vars.verbose_tts:
            sys.stdout = sys.__stdout__
            
        playback_queue.put(file_path)

playback_thread = threading.Thread(target=play_audio_from_queue)
playback_thread.daemon = True
playback_thread.start()


def write_conversation(sender, message, timestamp): 
    help.write_to_file(sender, message, timestamp)
    help.write_to_current_chat_history(sender, message)
    help.write_to_json(sender, message)
    help.trim_chat_history()

def print_to_console(sender, timestamp, message=None):
    print("====================================================================")
    if sender == vars.user_name:
        print(Fore.YELLOW + f"{vars.user_name} " + Style.RESET_ALL + f"({timestamp})\n" + message)

    else:
        print(Fore.MAGENTA + f"{vars.ai_name} " + Style.RESET_ALL + f"({timestamp})")
        
    if vars.verbose_token:
        print(Fore.CYAN + f'[Tokens: {help.get_token_count(help.construct_message(sender, message, timestamp))} ({help.get_token_count(help.build_system_prompt() + help.build_user_prompt())}/{vars.llm_n_ctx})]\n' + Style.RESET_ALL)

def infer(message, timestamp):
    help.trim_chat_history()    
    print_to_console(vars.user_name, timestamp, message)
    write_conversation(vars.user_name, message, timestamp)
    prompt_llm(timestamp)
        
def prompt_llm(timestamp):    
    
    print_to_console(vars.ai_name, timestamp)
    
    messages = []
    messages.extend(help.build_system_prompt_with_objects())
    messages.extend(help.build_user_prompt_with_objects())
    
    if vars.verbose_history:
        print(Fore.CYAN + "CHAT HISTORY AS TEXT:" + Style.RESET_ALL)
        print(help.build_system_prompt() + help.build_user_prompt())
    
    first_token_processed = False
    second_token_processed = False
    reply = ""
    char = ""
    char_array = []
        
    for chunk in vars.llm.create_chat_completion(
        messages = messages,
        temperature=vars.llm_temperature,
        top_p=vars.llm_top_p,
        top_k=vars.llm_top_k,
        stream=vars.llm_stream,
        stop=vars.llm_stop,
        max_tokens=vars.llm_max_tokens,
        presence_penalty=vars.llm_presence_penalty,
        frequency_penalty=vars.llm_frequency_penalty,
        repeat_penalty=vars.llm_repeat_penalty,
        tfs_z=vars.llm_tfs_z,
        mirostat_mode=vars.llm_mirostat_mode,
        mirostat_eta=vars.llm_mirostat_eta,
        mirostat_tau=vars.llm_mirostat_tau
    ):
        if not first_token_processed:
            first_token_processed = True
        elif first_token_processed and not second_token_processed and 'content' in chunk['choices'][0]['delta']:
            char = chunk['choices'][0]['delta']['content'].lstrip()
            print(char, end="", flush=True)
            second_token_processed = True
        elif first_token_processed and second_token_processed and 'content' in chunk['choices'][0]['delta']:
            char = chunk['choices'][0]['delta']['content']
            print(char, end="", flush=True)

        if first_token_processed:
            reply += char
            char_array.append(char)
        
    if reply is None:
        print(Fore.CYAN + f"{vars.ai_name} refuses to reply." + Style.RESET_ALL)
    else:
        print()
        
        write_conversation(vars.ai_name, reply, timestamp)   
                     
        reply = help.filter_text(reply)
        
        invoke_text_to_speech(reply)
        
        help.sentiment_calculation(reply)
        
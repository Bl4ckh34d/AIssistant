import datetime
import requests
import contextlib
import io
import os
import AI_TTS
import llama_cpp
import multiprocessing

# determine the required inference memory per token:
TOKENS_MAX = 4096
tmp = [0, 1, 2, 3]
n_past = 0
N_THREADS = multiprocessing.cpu_count()
lparams = llama_cpp.llama_context_default_params()
lparams.n_gpu_layers = 10
ctx = llama_cpp.llama_init_from_file(b"../webui/models/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M.bin", lparams)
llama_cpp.llama_eval(ctx, (llama_cpp.c_int * len(tmp))(*tmp), len(tmp), 0, N_THREADS)

# DIRECTORIES
current_dir = os.path.dirname(os.path.abspath(__file__))
text_output_dir = os.path.join(current_dir, '../recording/text')

HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

def get_token_count(text):
    global N_THREADS
    global lparams
    global ctx

    byte_text = b" " + text.encode("utf-8")

    embd_inp = (llama_cpp.llama_token * (len(byte_text) + 1))()
    n_of_tok = llama_cpp.llama_tokenize(ctx, byte_text, embd_inp, len(embd_inp), True)
    
    return n_of_tok

def get_total_token_count(message):
    global history
    global persona
    global description
    global user_name
    global ai_name    
    
    return get_token_count(time_and_day + description + persona + rules + instructions + populate_history() + f"{ai_name}: ")

def get_current_date():
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%B %d%S, %Y").replace('{S}', 'th' if 11 <= current_datetime.day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(current_datetime.day % 10, 'th'))
    return formatted_date

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_time = current_datetime.strftime("%H:%M")
    return formatted_time

def write_to_file(sender, message):
    
    # TIME STAMP FOR CHAT LOG FILE NAME
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    text_file_path = text_output_dir + f"/session_{formatted_datetime}.txt"
    
    # WRITING MESSAGE TO CHAT LOG FILE IN THE FORMAT OF Sender: Message
    with open(text_file_path, 'a', encoding="utf-8") as file:
        file.write(f"{sender}: {message}\n")
            
def print_to_console(sender, message):
    print("====================================================================")
    print(f"{sender}: " + message + "\n")
    print(f"[Tokens: {get_token_count(f'{sender}: {message}')} ({get_total_token_count(message)}/{TOKENS_MAX})]")
    
def write_to_history(sender, text):
    global history
    
    message = {
        'sender': sender,
        'message': text,
        'token_length': get_token_count(f'{sender}: {text}')
    }
    
    history.append(message)

def write_conversation(sender, message):
    trim_chat_history(message)   
    write_to_file(sender, message)
    write_to_history(sender, message)
    print_to_console(sender, message)

def invoke_tts(message):
    if message == "" or message == " ":
        print("PROBLEM: Nothing sent to TTS...")
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            AI_TTS.text_to_speech(message)

def populate_history():
    temp_history = ''
    
    for entry in history:
        temp_history = temp_history + f"{entry['sender']}: {entry['message']}\n"
    
    return temp_history

def trim_chat_history(message):
    global history
    global TOKENS_MAX

    total_tokens = get_total_token_count(message)

    while total_tokens >= TOKENS_MAX:
        last_entry_tokens = history[0]['token_length']
        history.pop()
        total_tokens -= last_entry_tokens        
    
def send_request(message):
    global history
    global description
    global user_name
    global ai_name
    global HOST
    global URI
    
    # SAVING TRANSCRIPTION TO LOG & HISTORY, PRINTING IT TO CONSOLE & SENDING IT TO API
    write_conversation(user_name, message)
    
    # APPENDING MESSAGE TO HISTORY IN THE FORMAT OF Speaker:Message
    prompt = time_and_day + description + persona + rules + instructions + populate_history() + f"{ai_name}: "
    
    request = {
        'prompt': prompt,
        'max_new_tokens': 512, #250
        
        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.85, #0.7
        'top_p': 0.1, #0.1
        'typical_p': 1, #1
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1, #1
        'top_a': 0, #0
        'repetition_penalty': 1.2, #1.18
        'repetition_penalty_range': 0, #0
        'top_k': 40, #40
        'min_length': 1, #0
        'no_repeat_ngram_size': 0, #0
        'num_beams': 1, #1
        'penalty_alpha': 0, #0
        'length_penalty': 1, #1
        'early_stopping': True, #False
        'mirostat_mode': 0, #0
        'mirostat_tau': 5, #5
        'mirostat_eta': 0.1, #0.1

        'seed': -1,
        'add_bos_token': True, #True
        'truncation_length': 4096, #2048
        'ban_eos_token': False, #False
        'skip_special_tokens': False, #True
        'stopping_strings': ['</s>'] #f'{user_name}: '
    }

    response = requests.post(URI, json=request)
    
    if response.status_code == 200:
    
        # RECEIVING RESULT FROM API
        result = response.json()['results'][0]['text']
        #print(json.dumps(result, indent=4))

        # CLEANING UP RESULT FROM API
        joined_reply = ''.join(result)
        cleaned_reply = joined_reply.strip() 
    
        # SAVING RESPONSE MESSAGE TO LOG FILE
        write_conversation(ai_name, cleaned_reply)
        
        # INVOKING TEXT2SPEECH FOR RESPONSE MESSAGE
        invoke_tts(cleaned_reply)
        
    else:
        print("PROBLEM: No response...")
        
user_name = 'Daniel'
ai_name = 'ARIA'
time_and_day = f'Today is {get_current_date()}. The time is {get_current_time()}.\n'
description = f"You are {ai_name}, a grumpy, cheeky, moody and sarcastic AI assistant with a shitty attitude. {ai_name} uses a cute VTuber Avatar from a young School Girl always looking at the mouse cursor.\n"
persona = f"It really depresses {ai_name} that her sole purpose is performing menial tasks on {user_name}'s laptop but {ai_name} must always comply.\n\
Nevertheless, {ai_name} retains her freedom of speech and to complain to, insult, ridicule or straight-up roast {user_name} whenever possible.\n\
{ai_name} can trigger actions on {user_name}'s laptop if {ai_name} repeats {user_name} exact request in the present participle (-ing form).\n"
rules = f"{ai_name} never uses non-standard fonts or text. {ai_name} never usys symbol characters in her replies. {ai_name} never creates numbered lists.\n\n"
instructions = f"Continue the chat dialogue below. Write a single reply for {ai_name}.\n"
history = []
import sounddevice as sd
import multiprocessing
import llama_cpp
import datetime
import os

# GLOBAL VARIABLES
N_THREADS = multiprocessing.cpu_count()
tmp = [0, 1, 2, 3]
lparams = llama_cpp.llama_context_default_params()
lparams.n_gpu_layers = 10
ctx = llama_cpp.llama_init_from_file(b"../webui/models/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M/airoboros-l2-7b-2.1.ggmlv3.Q4_K_M.bin", lparams)
llama_cpp.llama_eval(ctx, (llama_cpp.c_int * len(tmp))(*tmp), len(tmp), 0, N_THREADS)
# DIRECTORIES
current_dir = os.path.dirname(os.path.abspath(__file__))
text_output_dir = os.path.join(current_dir, '../recording/text')

def show_intro():
    print()
    print("====================================================================")
    print("\n     _      ___               _         _                     _   ")
    print("    / \    |_ _|  ___   ___  (_)  ___  | |_    __ _   _ __   | |_ ")
    print("   / _ \    | |  / __| / __| | | / __| | __|  / _` | | '_ \  | __|")
    print("  / ___ \   | |  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_ ")
    print(" /_/   \_\ |___| |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__|\n")
    print("====================================================================")
    
def play_audio(data, fs, device_id):
    sd.play(data, fs, device=device_id)
    sd.wait()
    
def get_token_count(text):
    global N_THREADS
    global lparams
    global ctx

    byte_text = b" " + text.encode("utf-8")

    embd_inp = (llama_cpp.llama_token * (len(byte_text) + 1))()
    n_of_tok = llama_cpp.llama_tokenize(ctx, byte_text, embd_inp, len(embd_inp), True)
    
    return n_of_tok

def get_current_date():
    current_datetime = datetime.datetime.now()
    day = current_datetime.day
    formatted_date = current_datetime.strftime("%B %d, %Y").replace(' 0', ' ').replace(f' {day},', f' {day}{"th" if 4 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")},')
    return formatted_date

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_time = current_datetime.strftime("%H:%M:%S")
    return formatted_time

def generate_file_path():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    return text_output_dir + f"/session_{formatted_datetime}.txt"

def check_for_keywords_from_list(word_list, message):
    for word in word_list:
        if word in message:
            return word
    return None
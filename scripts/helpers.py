import sounddevice as sd
import variables as vars
import datetime
import llama_cpp
import AI_LLM

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
    byte_text = b" " + text.encode("utf-8")
    embd_inp = (llama_cpp.llama_token * (len(byte_text) + 1))()
    n_of_tok = llama_cpp.llama_tokenize(vars.ctx, byte_text, embd_inp, len(embd_inp), True)
    return n_of_tok

def generate_file_path():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    return vars.directory_text + f"/session_{formatted_datetime}.txt"

def check_for_keywords_from_list(word_list, message):
    for word in word_list:
        if word in message:
            return word
    return None

def assemble_prompt_for_LLM():
    prompt = "#### Instruction:\n" + vars.time_and_day + vars.description + vars.persona + vars.rules + vars.instructions + "\n#### Chat History:\n" + AI_LLM.populate_history() + "\n#### Response:\n" + f"{vars.ai_name}: "
    return prompt

def populate_history():
    temp_history = ''
    
    for entry in vars.history:
        temp_history = temp_history + f"{entry['sender']}: {entry['message']}\n"
    
    return temp_history
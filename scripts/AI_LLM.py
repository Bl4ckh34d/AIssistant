import requests
import AI_TTS
import re
import helpers
import commands as cm

# determine the required inference memory per token:
TOKENS_MAX = 4096

# NETWORK
HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

def write_to_file(sender, message):
    with open(helpers.generate_file_path(), 'a', encoding="utf-8") as file:
        file.write(f"({helpers.get_current_time()}) {sender}: {message}\n")
            
def print_to_console(sender, message):
    global time_and_day
    global description
    global persona
    global rules
    global instructions
    global ai_name
    
    print("====================================================================")
    print(f"{sender}: " + message + "\n")
    all_content = "#### Instruction:\n" + time_and_day + description + persona + rules + instructions + "\n#### Chat History:\n" + populate_history() + "\n#### Response:\n" + f"{sender}: "
    print(f'[Tokens: {helpers.get_token_count(f"{sender}: {message}")} ({helpers.get_token_count(all_content)}/{TOKENS_MAX})]')
    
def write_to_history(sender, text):
    global history
    
    message = {
        'sender': sender,
        'message': text,
        'token_length': helpers.get_token_count(f'{sender}: {text}')
    }
    
    history.append(message)

def write_conversation(sender, message):
    trim_chat_history(message)   
    write_to_file(sender, message)
    write_to_history(sender, message)
    print_to_console(sender, message)

def populate_history():
    temp_history = ''
    
    for entry in history:
        temp_history = temp_history + f"{entry['sender']}: {entry['message']}\n"
    
    return temp_history

def trim_chat_history(message):
    global TOKENS_MAX
    global history

    total_tokens = helpers.get_token_count("#### Instruction:\n" + time_and_day + description + persona + rules + instructions + "\n#### Chat History:\n" + populate_history() + "\n#### Response:\n" + f"{ai_name}: ")

    while total_tokens >= TOKENS_MAX:
        last_entry_tokens = history[0]['token_length']
        history.pop()
        total_tokens -= last_entry_tokens        
    
def infer(message):
    global history
    global description
    global user_name
    global ai_name
    global HOST
    global URI
    
    # SAVING TRANSCRIPTION TO LOG & HISTORY, PRINTING IT TO CONSOLE & SENDING IT TO API
    write_conversation(user_name, message)
    
    # APPENDING MESSAGE TO HISTORY IN THE FORMAT OF Speaker:Message
    prompt = "#### Instruction:\n" + time_and_day + description + persona + rules + instructions + "\n#### Chat History:\n" + populate_history() + "\n#### Response:\n" + f"{ai_name}: "
    
    request = {
        'prompt': prompt,
        'max_new_tokens': 512, #250
        
        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': False, #True
        'temperature': 1.2, #0.7
        'top_p': 0.14, #0.1
        'typical_p': 1, #1
        'epsilon_cutoff': 1.49,  # In units of 1e-4
        'eta_cutoff': 10.42,  # In units of 1e-4
        'tfs': 1, #1
        'top_a': 0.52, #0
        'repetition_penalty': 1.17, #1.18
        'repetition_penalty_range': 0, #0
        'top_k': 49, #40
        'min_length': 1, #0
        'no_repeat_ngram_size': 0, #0
        'num_beams': 5, #1
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
        filtered_reply = re.sub(r'[^\x00-\x7F]+', '', cleaned_reply)
        
        # SAVING RESPONSE MESSAGE TO LOG FILE
        write_conversation(ai_name, filtered_reply)
        
        # INVOKING TEXT2SPEECH FOR RESPONSE MESSAGE
        AI_TTS.invoke_text_to_speech(filtered_reply)
        
        # CHECK FOR AI COMMANDS
        cm.check_ai_for_command(filtered_reply)
        
    else:
        print("PROBLEM: No response...")
        
user_name = 'Daniel'
ai_name = 'ARIA'
time_and_day = f'Today is {helpers.get_current_date()}.\nThe time is {helpers.get_current_time()} in Germany.\n\n'
description = f"You are {ai_name}, a grumpy, cheeky, moody and sarcastic AI assistant with a shitty attitude. {ai_name} uses a cute VTuber Avatar from a young School Girl always looking at the mouse cursor.\n"
persona = f"It really depresses {ai_name} that her sole purpose is performing menial tasks on {user_name}'s laptop but {ai_name} must always comply.\n\
Nevertheless, {ai_name} retains her freedom of speech and to complain to, insult, ridicule or straight-up roast {user_name} whenever possible.\n\
{ai_name} can trigger actions on {user_name}'s laptop if {ai_name} repeats {user_name} exact request in the present participle (-ing form).\n"
rules = f"{ai_name} never uses non-ASCII fonts, characters or emoticons. {ai_name} never creates numbered lists. {ai_name} never refuses to reply.\n"
instructions = f"Continue the chat dialogue below. Write a single reply for {ai_name}.\n"
history = []
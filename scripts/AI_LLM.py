import requests
import AI_TTS
import re
import helpers
import commands as cm
import variables as vars

def write_to_file(sender, message):
    with open(helpers.generate_file_path(), 'a', encoding="utf-8") as file:
        file.write(f"({helpers.get_current_time()}) {sender}: {message}\n")
            
def print_to_console(sender, message):
    print("====================================================================")
    print(f"{sender}: " + message + "\n")
    all_content = helpers.assemble_prompt_for_LLM()
    print(f'[Tokens: {helpers.get_token_count(f"{sender}: {message}")} ({helpers.get_token_count(all_content)}/{vars.TOKENS_MAX})]')
    
def write_to_history(sender, text):    
    message = {
        'sender': sender,
        'message': text,
        'token_length': helpers.get_token_count(f'{sender}: {text}')
    }
    
    vars.history.append(message)

def write_conversation(sender, message):  
    write_to_file(sender, message)
    write_to_history(sender, message)
    trim_chat_history() 
    print_to_console(sender, message)

def populate_history():
    temp_history = ''
    
    for entry in vars.history:
        temp_history = temp_history + f"{entry['sender']}: {entry['message']}\n"
    
    return temp_history

def trim_chat_history():
    total_tokens = helpers.get_token_count("#### Instruction:\n" + vars.time_and_day + vars.description + vars.persona + vars.rules + vars.instructions + "\n#### Chat History:\n" + populate_history() + "\n#### Response:\n" + f"{vars.ai_name}: ")

    while total_tokens >= vars.TOKENS_MAX:
        last_entry_tokens = vars.history[0]['token_length']
        vars.history.pop()
        total_tokens -= last_entry_tokens        
    
def infer(message):
    # SAVING TRANSCRIPTION TO LOG & HISTORY, PRINTING IT TO CONSOLE & SENDING IT TO API
    write_conversation(vars.user_name, message)
    
    # APPENDING MESSAGE TO HISTORY IN THE FORMAT OF Speaker:Message
    prompt = helpers.assemble_prompt_for_LLM()
    
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

    response = requests.post(vars.URI, json=request)
    
    if response.status_code == 200:
    
        # RECEIVING RESULT FROM API
        result = response.json()['results'][0]['text']
        #print(json.dumps(result, indent=4))

        # CLEANING UP RESULT FROM API
        joined_reply = ''.join(result)
        cleaned_reply = joined_reply.strip() 
        filtered_reply = re.sub(r'[^\x00-\x7F]+', '', cleaned_reply)
        
        # SAVING RESPONSE MESSAGE TO LOG FILE
        write_conversation(vars.ai_name, filtered_reply)
        
        # INVOKING TEXT2SPEECH FOR RESPONSE MESSAGE
        AI_TTS.invoke_text_to_speech(filtered_reply)
        
        # CHECK FOR AI COMMANDS
        cm.check_ai_for_command(filtered_reply)
        
    else:
        print("PROBLEM: No response...")
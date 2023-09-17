import requests
import AI_TTS
import re
import helpers
import variables as vars
from transformers import AutoModelForCausalLM, AutoTokenizer

def write_conversation(sender, message):  
    write_to_file(sender, message)
    write_to_history(sender, message)
    helpers.write_to_longterm_memory(sender, message)
    helpers.trim_chat_history() 
    print_to_console(sender, message)

def write_to_file(sender, message):
    with open(helpers.generate_file_path("txt"), 'a', encoding="utf-8") as file:
        file.write(f"{sender}: {message}\n") #f"({helpers.get_current_time()}) {sender}: {message}\n"
        
def write_to_history(sender, text):    
    message = {
        'sender': sender,
        'message': text,
        'token_length': helpers.get_token_count(f'{sender}: {text}')
    }
    
    vars.history.append(message)

def print_to_console(sender, message):
    print("====================================================================")
    print(f"{sender}: " + message)
    print(f'[Tokens: {helpers.get_token_count(f"{sender}: {message}")} ({helpers.get_token_count(helpers.assemble_prompt_for_LLM())}/{vars.TOKENS_MAX})]\n')

def infer(message):
    if message == "":
        #send_request(True)
        prompt_llm(True)
    else:
        write_conversation(vars.user_name, message)
        prompt_llm()
        #send_request()
        
def prompt_llm(init):
    if init:
        prompt = helpers.assemble_prompt_for_LLM() + f"Write a greeting to {vars.user_name} depending on your current mood{vars.ai_name}.\n{vars.ai_name}:"
    else:
        prompt = helpers.assemble_prompt_for_LLM() + f"{vars.ai_name}:"
        
    
    llm_output = vars.llm(prompt, max_tokens=300, stop=[f'{vars.user_name}:'], echo=True)
    answer = llm_output["choices"][0]["text"][len(prompt):]
    
    # CLEANING UP RESULT FROM API
    joined_reply = ''.join(answer)
    cleaned_reply = joined_reply.strip() 
    filtered_reply = re.sub(r'[^\x00-\x7F]+', '', cleaned_reply)
    
    # CLEARING OUT EMOJIS, PARENTHESE, ASTERISKS, ETC.
    filtered_reply = helpers.filter_text(filtered_reply)
    
    # SENTIMENT ANALYSIS
    helpers.sentiment_calculation(filtered_reply)
    
    # SAVING RESPONSE MESSAGE TO LOG FILE
    write_conversation(vars.ai_name, filtered_reply)
    
    # INVOKING TEXT2SPEECH FOR RESPONSE MESSAGE
    AI_TTS.invoke_text_to_speech(filtered_reply)

def send_request(init=False):  
    if init:
        prompt = helpers.assemble_prompt_for_LLM() + f"Write a greeting to {vars.user_name} depending on your current mood{vars.ai_name}.\n{vars.ai_name}:"
    else:
        prompt = helpers.assemble_prompt_for_LLM() + f"{vars.ai_name}:"
    
    request = {
        'prompt': prompt,
        'max_new_tokens': 250, #250
        
        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True, #True
        'temperature': 0.6, #0.7
        'top_p': 0.1, #0.1
        'typical_p': 1, #1
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1, #1
        'top_a': 0, #0
        'repetition_penalty': 1.18, #1.18
        'repetition_penalty_range': 0, #0
        'top_k': 40, #40
        'min_length': 0, #0
        'no_repeat_ngram_size': 0, #0
        'num_beams': 5, #1
        'penalty_alpha': 0, #0
        'length_penalty': 1.18, #1
        'early_stopping': True, #False
        'mirostat_mode': 2, #2
        'mirostat_tau': 5, #5
        'mirostat_eta': 0.1, #0.1

        'seed': -1,
        'add_bos_token': True, #True
        'truncation_length': 4096, #2048
        'ban_eos_token': False, #False
        'skip_special_tokens': False, #True
        'stopping_strings': [f'{vars.user_name}:']
    }

    response = requests.post(vars.URI, json=request)
    
    if response.status_code == 200:
    
        # RECEIVING RESULT FROM API
        result = response.json()['results'][0]['text']

        # CLEANING UP RESULT FROM API
        joined_reply = ''.join(result)
        cleaned_reply = joined_reply.strip() 
        filtered_reply = re.sub(r'[^\x00-\x7F]+', '', cleaned_reply)
        
        # CLEARING OUT EMOJIS, PARENTHESE, ASTERISKS, ETC.
        filtered_reply = helpers.filter_text(filtered_reply)
        
        # SENTIMENT ANALYSIS
        helpers.sentiment_calculation(filtered_reply)
        
        # SAVING RESPONSE MESSAGE TO LOG FILE
        write_conversation(vars.ai_name, filtered_reply)
        
        # INVOKING TEXT2SPEECH FOR RESPONSE MESSAGE
        AI_TTS.invoke_text_to_speech(filtered_reply)
        
    else:
        print("PROBLEM: No response...")
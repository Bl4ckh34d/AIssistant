import AI_TTS
import re
import helpers
import variables as vars

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
        prompt_llm(True)
    else:
        write_conversation(vars.user_name, message)
        prompt_llm(False)
        
def prompt_llm(init):
    if init:
        prompt = helpers.assemble_prompt_for_LLM() + vars.instructions_init + f"\n{vars.ai_name}:"
    else:
        prompt = helpers.assemble_prompt_for_LLM() + vars.instructions + f"{vars.ai_name}:"
    llm_output = vars.llm(prompt=prompt, max_tokens=300, stop=[f'{vars.user_name}:'], echo=False, mirostat_mode=2, mirostat_eta=0.1, mirostat_tau=5, temperature=0.7, top_p=0.95, frequency_penalty=0, presence_penalty=0, repeat_penalty=1.2, top_k=40)
    answer = llm_output["choices"][0]["text"]
    
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
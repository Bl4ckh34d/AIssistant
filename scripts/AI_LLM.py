import AI_TTS, re
import variables as vars, helpers as help
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

def write_conversation(sender, message):  
    write_to_file(sender, message)
    write_to_history(sender, message)
    help.write_to_longterm_memory(sender, message)
    help.trim_chat_history() 
    print_to_console(sender, message)

def write_to_file(sender, message):
    with open(help.generate_file_path("txt"), 'a', encoding="utf-8") as file:
        file.write(f"{sender}: {message}\n") #f"({helpers.get_current_time()}) {sender}: {message}\n"
        
def write_to_history(sender, text):    
    message = {
        'sender': sender,
        'message': text,
        'token_length': help.get_token_count(f'{sender}: {text}')
    }
    
    vars.history_current.append(message)

def print_to_console(sender, message):
    print("====================================================================")
    if sender == vars.ai_name:
        print(Fore.YELLOW + f"{sender}: " + message + Style.RESET_ALL)
    else:
        print(Fore.GREEN + f"{sender}: " + message + Style.RESET_ALL)
    
    if vars.silent is False:
        print(Fore.CYAN + f'[Tokens: {help.get_token_count(f"{sender}: {message}")} ({help.get_token_count(help.assemble_prompt_for_LLM(False))}/{vars.llm_n_ctx})]\n' + Style.RESET_ALL)

def infer(message):
    help.trim_chat_history()
    
    if message == "INITIAL":
        prompt_llm(True)
    else:
        write_conversation(vars.user_name, message)
        prompt_llm(False)
        
def prompt_llm(init):
    prompt = help.assemble_prompt_for_LLM(init)
    
    if not vars.silent:
        print(Fore.CYAN + "CHAT HISTORY:" + Style.RESET_ALL)
        print(prompt) 
    
    llm_output = vars.llm(
        prompt=prompt,
        echo=False,
        max_tokens=vars.llm_max_tokens,
        stop=vars.llm_stop,
        mirostat_mode=vars.llm_mirostat_mode,
        mirostat_eta=vars.llm_mirostat_eta,
        mirostat_tau=vars.llm_mirostat_tau,
        temperature=vars.llm_temperature,
        top_p=vars.llm_top_p,
        top_k=vars.llm_top_k,
        frequency_penalty=vars.llm_frequency_penalty,
        presence_penalty=vars.llm_presence_penalty,
        repeat_penalty=vars.llm_repeat_penalty
    )
        
    answer = llm_output["choices"][0]["text"]
    
    if answer is None:
        print(Fore.CYAN + f"{vars.ai_name} refuses to reply." + Style.RESET_ALL)
    
    # CLEANING UP RESULT
    joined_reply = ''.join(answer)
    cleaned_reply = joined_reply.strip() 
    #filtered_reply = re.sub(r'[^\x00-\x7F]+', '', cleaned_reply)
    
    # SENTIMENT ANALYSIS
    help.sentiment_calculation(cleaned_reply)
    
    # SAVING RESPONSE MESSAGE TO LOG FILE
    write_conversation(vars.ai_name, cleaned_reply)
    
    # REMOVE CODE SNIPPETS BEFORE TTS
    final_reply = help.remove_code_snippets(cleaned_reply)
    
    # CLEARING OUT EMOJIS, PARENTHESE, ASTERISKS, ETC.
    final_reply = re.sub(r'[^\x00-\x7F]+', '', final_reply)
    final_reply = help.filter_text(final_reply)
    
    # INVOKING TEXT2SPEECH FOR RESPONSE MESSAGE
    AI_TTS.invoke_text_to_speech(final_reply)
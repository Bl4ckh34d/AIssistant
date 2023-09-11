import sounddevice as sd
import variables as vars
import datetime
import llama_cpp_ggml_cuda
import random
import datetime
import time

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
    
def get_current_date():
    current_datetime = datetime.datetime.now()
    day = current_datetime.day
    formatted_date = current_datetime.strftime("%B %d, %Y").replace(' 0', ' ').replace(f' {day},', f' {day}{"th" if 4 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")},')
    return formatted_date

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_time = current_datetime.strftime("%H:%M:%S")
    return formatted_time
    
def get_token_count(text):
    byte_text = b" " + text.encode("utf-8")
    embd_inp = (llama_cpp_ggml_cuda.llama_token * (len(byte_text) + 1))()
    n_of_tok = llama_cpp_ggml_cuda.llama_tokenize(vars.ctx, byte_text, embd_inp, len(embd_inp), True)
    return n_of_tok

def generate_file_path():
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    return vars.directory_text + f"/session_{formatted_datetime}.txt"

def check_for_keywords_from_list(word_list, message):
    message_lower = message.lower()
    for word in word_list:
        if word.lower() in message_lower:
            return word
    return None

def assemble_prompt_for_LLM():
    prompt = f'(Date: {get_current_date()}. Time: {get_current_time()})\n\n' + vars.persona + vars.active_mood + vars.rules + vars.instructions + populate_history() + f"{vars.ai_name}:"
    return prompt

def populate_history():
    temp_history = ''
    
    for entry in vars.history:
        temp_history = temp_history + f"{entry['sender']}: {entry['message']}\n"
    
    return temp_history

# Function to search for a tab with "youtube" in the title and make it active
def search_and_activate_tab(webdriver, keyword):
    tabs = webdriver.window_handles
    for tab in tabs:
        webdriver.switch_to.window(tab)
        if keyword in webdriver.title.lower():
            return
    # If no YouTube tab found, create a new tab with YouTube
    webdriver.execute_script(f"window.open('https://www.{keyword}.com');")
    
def swap_persona():
    # Define the persona descriptions
    persona_descriptions = [
        vars.happy_mood,
        vars.sad_mood,
        vars.angry_mood,
        vars.horny_mood,
        vars.bored_mood,
        vars.neutral_mood
    ]

    # Define the base weights
    base_weights = {
        vars.happy_mood: 0.3,
        vars.sad_mood: 0.15,
        vars.angry_mood: 0.05,
        vars.horny_mood: 0.15,
        vars.bored_mood: 0.18,
        vars.neutral_mood: 0.22
    }
    
    # Define the fluctuation budget
    fluctuation_budget = 0.2
    
    # Reduce the base weights to 0.8 total
    total_base_weight = sum(base_weights.values())
    reduction_factor = 0.8 / total_base_weight
    base_weights = {persona: weight * reduction_factor for persona, weight in base_weights.items()}

    # Shuffle the persona descriptions to randomize the order
    random.shuffle(persona_descriptions)

    # Calculate the number of personas
    num_personas = len(persona_descriptions)

    # Distribute the fluctuation budget randomly among the base weights
    for i, persona in enumerate(persona_descriptions):
        if i < num_personas - 1:
            # Generate a random weight within the remaining budget
            fluctuation = random.uniform(0, fluctuation_budget)
            fluctuation_budget -= fluctuation
        else:
            # Use the remaining budget for the last persona
            fluctuation = fluctuation_budget

        # Add the fluctuation to the base weight
        base_weights[persona] += fluctuation

    # Choose a random persona based on the fluctuated weights
    selected_persona = random.choices(persona_descriptions, list(base_weights.values()))[0]
    
    # Print the selected persona description
    if selected_persona == vars.happy_mood:
        print(f"({vars.ai_name} is happy)\n")
    if selected_persona == vars.sad_mood:
        print(f"({vars.ai_name} is sad)\n")
    if selected_persona == vars.angry_mood:
        print(f"({vars.ai_name} is angry)\n")
    if selected_persona == vars.horny_mood:
        print(f"({vars.ai_name} is aroused)\n")
    if selected_persona == vars.bored_mood:
        print(f"({vars.ai_name} is bored)\n")
    if selected_persona == vars.neutral_mood:
        print(f"({vars.ai_name} is neutral)\n")
        
    vars.active_mood = selected_persona
    
def cycle_personas():
    current_time = time.time()
    time_difference = current_time - vars.persona_saved_time
    if time_difference > vars.persona_current_change_time:
        
        swap_persona()
        vars.persona_saved_time = time.time()

        # Generate a random delay between 1 to 10 minutes (60 to 600 seconds)
        vars.persona_current_change_time = random.randint(vars.persona_min_change_time, vars.persona_max_change_time)
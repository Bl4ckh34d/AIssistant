import sounddevice as sd
import variables as vars
import datetime
import llama_cpp_ggml_cuda
import random
import datetime
import time
import re
import json
import os
import pygetwindow as gw
import psutil
from transformers import pipeline
import win32gui
import win32con
import win32process
import pyautogui

classifier_sentiment = pipeline("sentiment-analysis")

# MISC
def show_intro():
    print()
    print("====================================================================")
    print("\n     _      ___               _         _                     _   ")
    print("    / \    |_ _|  ___   ___  (_)  ___  | |_    __ _   _ __   | |_ ")
    print("   / _ \    | |  / __| / __| | | / __| | __|  / _` | | '_ \  | __|")
    print("  / ___ \   | |  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_ ")
    print(" /_/   \_\ |___| |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__|\n")
    print("====================================================================")

def get_token_count(text):
    byte_text = b" " + text.encode("utf-8")
    embd_inp = (llama_cpp_ggml_cuda.llama_token * (len(byte_text) + 1))()
    n_of_tok = llama_cpp_ggml_cuda.llama_tokenize(vars.ctx, byte_text, embd_inp, len(embd_inp), True)
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

def generate_file_path(filetype):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    return vars.directory_text + f"/session_{formatted_datetime}.{filetype}"

def split_to_sentences(message):
    sentences = []
    current_sentence = []
    consecutive_count = 0
    
    for char in message:
        current_sentence.append(char)
        if char in ('.', '!', '?'):
            consecutive_count += 1
        else:
            consecutive_count = 0

        if consecutive_count > 1:
            # Remove extra consecutive punctuation from the current sentence
            current_sentence = current_sentence[:-consecutive_count + 1]

            if sentences:
                # Add consecutive punctuation to the previous sentence
                sentences[-1] += ''.join(current_sentence).strip()
                current_sentence = []

    if current_sentence:
        sentences.append(''.join(current_sentence).strip())

    return sentences

def extract_date_from_filename(filename):
    date_str = filename.split('_')[1].split('.')[0]
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def memory_to_history(json_f, token_budget):
    message_list = []

    # Read the JSON file
    with open(json_f, 'r') as json_file:
        data = json.load(json_file)
                 
    for entry in data:
        if token_budget > 0:
            messages = entry['message']

            # Check if there's only one message in this entry
            if len(messages) == 1:
                sender = messages[0]['speaker']
                text = messages[0]['text']
                token_length = messages[0]['token']

                # Create a message dictionary for the single message
                message = {
                    'sender': sender,
                    'message': text,
                    'token_length': token_length
                }

                # Append the single message entry to your list variable
                if token_budget >= token_length:  
                    message_list.append(message)
                token_budget = token_budget - token_length
            else:
                # Assuming there are always two messages when there's more than one
                for i in range(0, len(messages), 2):
                    sender1 = messages[i]['speaker']
                    text1 = messages[i]['text']
                    token_length1 = messages[i]['token']

                    sender2 = messages[i + 1]['speaker']
                    text2 = messages[i + 1]['text']
                    token_length2 = messages[i + 1]['token']

                    # Create message dictionaries for both pairs
                    message = {
                        'sender': sender1,
                        'message': text1,
                        'token_length': token_length1
                    }
                    message_list.append(message)
                    message = {
                        'sender': sender2,
                        'message': text2,
                        'token_length': token_length2
                    }
                    message_list.append(message)
                    token_budget = token_budget - token_length2 - token_length1

    return message_list

def filter_text(input_text):
    # Define regular expressions to match emojis and *wink*
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # Emojis
                               u"\U0001F300-\U0001F5FF"  # Misc symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # Transport & map symbols
                               u"\U0001F700-\U0001F77F"  # Alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric shapes
                               u"\U0001F800-\U0001F8FF"  # Supplemental symbols & pictographs
                               "]+", flags=re.UNICODE) 
    
    text_in_asterisks_pattern = re.compile(r'\*([^*]+)\*')
    text_in_parentheses_pattern = re.compile(r'\(([^)]+)\)')
    hashtag_pattern = re.compile(r'#\w+')
    
    # Remove emojis, text in asterisks, and hashtags from the input text
    filtered_text = emoji_pattern.sub('', input_text)
    filtered_text = text_in_asterisks_pattern.sub('', filtered_text)
    filtered_text = text_in_parentheses_pattern.sub('', filtered_text)
    filtered_text = hashtag_pattern.sub('', filtered_text)
    
    return filtered_text


# AUDIO    
def play_audio(data, fs, device_id):
    sd.play(data, fs, device=device_id)
    sd.wait()
    
    
# LLM PROMPT
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
        vars.happy_mood: 0.1,
        vars.sad_mood: 0.1,
        vars.angry_mood: 0.05,
        vars.horny_mood: 0.05,
        vars.bored_mood: 0.2,
        vars.neutral_mood: 0.4
    }
    
    # Define the fluctuation budget
    fluctuation_budget = 0.1
    
    base_weights = {persona: weight for persona, weight in base_weights.items()}

    # Shuffle the persona descriptions to randomize the order
    random.shuffle(persona_descriptions)

    # Calculate the number of personas
    num_personas = len(persona_descriptions)

    # Distribute the fluctuation budget randomly among the base weights
    for i, persona in enumerate(persona_descriptions):
        if i < num_personas - 1:
            # Generate a random weight within the remaining budget
            fluctuation = random.uniform(-fluctuation_budget, fluctuation_budget)
            fluctuation_budget -= fluctuation
        else:
            # Use the remaining budget for the last persona
            fluctuation = fluctuation_budget

        # Add the fluctuation to the base weight
        base_weights[persona] += fluctuation

    # Choose a random persona based on the fluctuated weights
    selected_persona = random.choices(persona_descriptions, list(base_weights.values()))[0]
    
    # Print the selected persona description
    if not vars.silent:
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
 
def assemble_prompt_for_LLM():
    prompt = f'(Date:{get_current_date()}. Time:{get_current_time()})\n\n' + vars.persona + vars.active_mood + vars.rules + vars.instructions + populate_history()
    return prompt

# LLM HISTORY
def populate_history():
    temp_history = ''
    
    for entry in vars.history:
        temp_history = temp_history + f"{entry['sender']}:{entry['message']}\n"
    
    return temp_history

def trim_chat_history():
    total_tokens = get_token_count(assemble_prompt_for_LLM())

    while total_tokens >= vars.TOKENS_MAX:
        last_entry_tokens = vars.history[0]['token_length']
        vars.history.pop()
        total_tokens -= last_entry_tokens 


# LLM SENTIMENT ANALYSIS    
def sentiment_calculation(message):
    if message != "" and message != " ":
        total_sentiment = 0
        for sentence in split_to_sentences(message):
            sentiment = classifier_sentiment(sentence)
            if sentiment[0]['label'] == "POSITIVE":
                total_sentiment += sentiment[0]['score']
            else:
                total_sentiment -= sentiment[0]['score']
            if not vars.silent:
                print(f"SENTIMENT ANALYSIS: FEELING: {sentiment[0]['label']} and SCORE: {sentiment[0]['score']}")
        if not vars.silent:
            print(f"TOTAL SCORE: {total_sentiment}")
            print(f"AI SCORE: {vars.ai_mood_score}")
        vars.ai_mood_score += total_sentiment * random.gauss(0.1, 0.3)
        
        if vars.ai_mood_score > 5:
            vars.ai_mood_score = 5
        if vars.ai_mood_score <= 5 and vars.ai_mood_score > 4.5:
            vars.active_mood = random.choice([vars.happy_mood,vars.horny_mood,vars.neutral_mood,vars.bored_mood])
        if vars.ai_mood_score <= 4.5 and vars.ai_mood_score > 3:
            vars.active_mood = random.choice([vars.happy_mood,vars.neutral_mood,vars.bored_mood])
        if vars.ai_mood_score <= 3 and vars.ai_mood_score > 2:
            vars.active_mood = random.choice([vars.happy_mood,vars.neutral_mood])
        if vars.ai_mood_score <= 2 and vars.ai_mood_score > -2:
            vars.active_mood = random.choice([vars.happy_mood,vars.neutral_mood,vars.bored_mood])
        if vars.ai_mood_score <= -2 and vars.ai_mood_score > -3:
            vars.active_mood = random.choice([vars.neutral_mood,vars.bored_mood])
        if vars.ai_mood_score <= -3 and vars.ai_mood_score > -4.5:
            vars.active_mood = random.choice([vars.sad_mood,vars.neutral_mood,vars.bored_mood])
        if vars.ai_mood_score <= -4.5 and vars.ai_mood_score > -5:
            vars.active_mood = random.choice([vars.sad_mood,vars.angry_mood,vars.neutral_mood,vars.bored_mood])
        if vars.ai_mood_score < -5:
            vars.ai_mood_score = -5
    
    current_time = time.time()
    time_difference = current_time - vars.persona_saved_time
    if time_difference > vars.persona_current_change_time:
        
        swap_persona()
        vars.persona_saved_time = time.time()
        vars.persona_current_change_time = random.randint(vars.persona_min_change_time, vars.persona_max_change_time)


# LLM MEMORY
def write_to_longterm_memory(sender, message):
    # Get the current date in the 'YYYY-MM-DD' format
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Construct the filename using the current date
    json_filename = f"session_{current_date}.json"
    
    # Load existing chat history (if any)
    try:
        with open(generate_file_path("json"), 'r', encoding='utf-8') as json_file:
            memory = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty chat history
        memory = []
        
    # Create a new message block if there's no current block or if the current block belongs to the AI
    if not memory or memory[-1]['message'][-1]['speaker'] == vars.ai_name:
        memory.append({
            "message": [
                {
                    "speaker": sender,
                    "text": message,
                    "token": get_token_count(f"{sender}: {message}")
                }
            ]
        })
    else:
        # Append to the existing message block
        memory[-1]['message'].append({
            "speaker": sender,
            "text": message,
            "token": get_token_count(f"{sender}: {message}")
        })
    
    # Write the updated chat history back to the JSON file
    with open(generate_file_path("json"), 'w', encoding='utf-8') as json_file:
        json.dump(memory, json_file, indent=4)

    print(f"Chat history has been updated and saved to {json_filename}")

def build_memory():
    # Get a list of all JSON files in the specified directory
    json_files = [filename for filename in os.listdir(vars.directory_text) if filename.endswith('.json')]

    # Create a dictionary to store files and their ages
    file_ages = {}

    # Calculate the age of each file and store it in the dictionary
    for json_file in json_files:
        file_date = extract_date_from_filename(json_file)
        age = datetime.datetime.now() - file_date
        file_ages[json_file] = age
    
    # Sort the files based on their ages (newest first)    
    sorted_files = sorted(file_ages.items(), key=lambda x: x[1], reverse=True)

    # Initialize variables for today, yesterday, and the rest
    today_file = None
    recent_files = []
    rest_files = []
    
    # Separate the files into today, yesterday, and the rest
    for file, age in sorted_files:
        if age.days == 0:
            today_file = file
        elif age.days >= 1 and age.days <= 5:
            recent_files.append(file)
        else:
            rest_files.append(file)

    # Select one random file from the rest
    if rest_files:
        random_rest_file = random.choice(rest_files)
    if recent_files:
        random_recent_file = random.choice(recent_files)

    # Check available Token count
    token_used = get_token_count(assemble_prompt_for_LLM() + f"Write a random greeting to {vars.user_name} depending on your current mood{vars.ai_name}.\n{vars.ai_name}:")
    total_tokens = 4096
    token_budget = total_tokens - token_used
    today_budget = (token_budget * 70) / 100
    recent_budget = (token_budget * 15) / 100
    rest_budget = token_budget - today_budget - recent_budget
    if today_budget + recent_budget + rest_budget > token_budget:
        today_budget -= 10
    # Fill vars.history.extend(memory_to_history(os.path.join(vars.directory_text, random_file)))

    # Construct file paths if needed
    if rest_files:
        mem = memory_to_history(os.path.join(vars.directory_text, random_rest_file), rest_budget)
        vars.history.extend(mem)
    if recent_files:
        mem = memory_to_history(os.path.join(vars.directory_text, random_recent_file), recent_budget)
        vars.history.extend(mem)
    if today_file:
        mem = memory_to_history(os.path.join(vars.directory_text, today_file), today_budget)
        vars.history.extend(mem)

   
# COMMANDS
def check_for_keywords_from_list(word_list, message):
    message_lower = message.lower()
    for word in word_list:
        if word.lower() in message_lower:
            return word
    return None


# PROCESSES
def gather_pids():
    vars.init_pids = psutil.pids()
    for process in psutil.process_iter(attrs=['pid', 'name']):
        print(f"PID: {process.info['pid']}   NAME: {process.info['name']}")

def compare_pids():   
    vars.comp_pids = psutil.pids()
    
    new_pids = [pid for pid in vars.comp_pids if pid not in vars.init_pids]
    
    if not vars.silent:
        for pid in new_pids:
            print("new PID: ", pid)
    
    return new_pids

def close_pids(pid_list, search_term):
    gather_pids()
    find_pids(pid_list, search_term)
    for pid in pid_list:
        if psutil.pid_exists(pid):
            try:
                # Terminate the process
                process = psutil.Process(pid)
                process.terminate()
                if not vars.silent:
                    print(f"Process with PID {pid} has been terminated.")
            except psutil.NoSuchProcess:
                if not vars.silent:
                    print(f"No process found with PID {pid}.")
        else:
            print(f"Process with PID {pid} does not exist.")
            
def focus_pids(pid_list, search_term):
    gather_pids()
    find_pids(pid_list, search_term)
    for pid in pid_list:
        window_handles = find_window_handle(pid)            
        if window_handles:
            # Check if the window is in fullscreen mode (maximized)
            window_state = win32gui.GetWindowPlacement(window_handles[0])
            if window_state[1] == win32con.SW_SHOWMAXIMIZED:
                # Bring the first matching window to the foreground
                win32gui.ShowWindow(window_handles[0], win32con.SW_RESTORE)
                pyautogui.press("alt")
                win32gui.SetForegroundWindow(window_handles[0])
                window_state = win32gui.GetWindowPlacement(window_handles[0])
                if window_state[1] != win32con.SW_SHOWMAXIMIZED:
                    # Force the window into fullscreen mode (maximize)
                    win32gui.ShowWindow(window_handles[0], win32con.SW_MAXIMIZE)
            else:
                # Bring the first matching window to the foreground
                win32gui.ShowWindow(window_handles[0], win32con.SW_RESTORE)
                pyautogui.press("alt")
                win32gui.SetForegroundWindow(window_handles[0])
        else:
            print(f"No window found with PID {pid}.")
            
def find_window_handle(pid):
    def callback(hwnd, hwnd_list):
        try:
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if win32gui.IsWindowVisible(hwnd) and window_pid == pid:
                hwnd_list.append(hwnd)
        except win32process.error:
            pass
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)
    return hwnd_list
            
def find_pids(target_list, search_term):
    # Initialize an empty dictionary to store PIDs and their names
    pid_name_dict = {}

    # Get a list of all running processes and their names
    for process in psutil.process_iter(attrs=['pid', 'name', 'status']):
        if process.info['status'] == "running":
            try:
                pid = process.info['pid']
                name = process.info['name']
                pid_name_dict[pid] = name
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    # Find PIDs that contain the keyword in their process name
    matching_pids = [pid for pid, name in pid_name_dict.items() if search_term.lower() in name.lower()]
    matching_names = [name for pid, name in pid_name_dict.items() if search_term.lower() in name.lower()]

    if not vars.silent:
        for match in matching_names:
            print("Process name:", match)

    # Clear the external list and extend it with the matching PIDs
    target_list.clear()
    target_list.extend(matching_pids)
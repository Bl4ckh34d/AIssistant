import datetime, time, llama_cpp, random, re, json, os, psutil, win32gui, win32con, win32process, pyautogui, subprocess, pyaudio
import sounddevice as sd, variables as vars
from transformers import pipeline
from colorama import Fore, Back, Style, init

# Initialize colorama
init()

classifier_sentiment = pipeline("sentiment-analysis", model=vars.sa_model_path, tokenizer=vars.sa_model_path)

# SETUP
def setup_user_name():
    subprocess.call('cls', shell=True)
    print()
    print(Fore.YELLOW + "====================================================================")
    print("\n     _      ___               _         _                     _   ")
    print("    / \    |_ _|  ___   ___  (_)  ___  | |_    __ _   _ __   | |_ ")
    print("   / _ \    | |  / __| / __| | | / __| | __|  / _` | | '_ \  | __|")
    print("  / ___ \   | |  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_ ")
    print(" /_/   \_\ |___| |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__|\n")
    print("====================================================================" + Style.RESET_ALL)
    print()
    name = input("Enter your " + Fore.MAGENTA + "NAME" + Style.RESET_ALL + ": ")
    if name != "" and name != " ":
        vars.user_name = name
    
    subprocess.call('cls', shell=True)

def setup_audio_input():
    print(Fore.MAGENTA + "\nAvailable Audio Input Devices:" + Style.RESET_ALL)
    print()
    
    p = pyaudio.PyAudio()
    device_ids = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            print("ID: " + Fore.MAGENTA + f"{device_info['index']}" + Style.RESET_ALL + f", Name: {device_info['name']}")
            device_ids.append(device_info['index'])
    p.terminate()
    print()
    audio_device = input(f"Enter your prefered " + Fore.MAGENTA + "AUDIO INPUT DEVICE ID" + Style.RESET_ALL + ": ")
    if audio_device.isdigit() and audio_device in device_ids:
        vars.AUDIO_INPUT_DEVICE_ID = int(audio_device)
    else:
        vars.AUDIO_INPUT_DEVICE_ID = device_ids[0]
    
    subprocess.call('cls', shell=True)
    
def setup_audio_output():
    print(Fore.MAGENTA + "\nAvailable Audio Output Devices:" + Style.RESET_ALL)
    print()
    
    p = pyaudio.PyAudio()
    device_ids = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxOutputChannels'] > 0:
            print("ID: " + Fore.MAGENTA + f"{device_info['index']}" + Style.RESET_ALL + f", Name: {device_info['name']}")
            device_ids.append(device_info['index'])
    p.terminate()
    print()
    audio_device = input(f"Enter your prefered " + Fore.MAGENTA + "AUDIO OUTPUT DEVICE ID" + Style.RESET_ALL + ": ")
    if audio_device.isdigit() and audio_device in device_ids:
        vars.AUDIO_OUTPUT_DEVICE_ID = int(audio_device)
    else:
        vars.AUDIO_OUTPUT_DEVICE_ID = device_ids[0]
    
    subprocess.call('cls', shell=True)

def get_token_count(text):
    if vars.llm_model_file_type == "gguf":
        text = text.encode('utf-8')
        llm_embd_inp = (llama_cpp.llama_token * (len(text) + 1))()
        return llama_cpp.llama_tokenize(vars.llm_ctx, text, llm_embd_inp, len(llm_embd_inp), True)

def get_current_date():
    current_datetime = datetime.datetime.now()
    day = current_datetime.day
    formatted_date = current_datetime.strftime("%B %d, %Y").replace(' 0', ' ').replace(f' {day},', f' {day}{"th" if 4 <= day % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")},')
    return formatted_date

def get_current_timezone():
    now = datetime.datetime.now()
    local_offset = now.astimezone().utcoffset()
    formatted_offset = local_offset.total_seconds() // 3600
    formatted_offset = f"UTC{'+' if formatted_offset >= 0 else ''}{int(formatted_offset)}"
    return formatted_offset

def get_current_time():
    current_datetime = datetime.datetime.now()
    formatted_time = current_datetime.strftime("%H:%M:%S") + " " + get_current_timezone()
    return formatted_time

def generate_file_path(filetype):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d")
    return vars.directory_text + f"/session_{formatted_datetime}.{filetype}"

def split_reply_to_chunks(message):
    chunk_pattern = r'(?<=[.!?,-](?!\w))+(?:\s|,)+'
    chunks = re.split(chunk_pattern, message)
    chunks = [chunk.strip() for chunk in re.split(chunk_pattern, message) if chunk.strip()]
    if vars.verbose_tts:
        print(chunks)
    return chunks

def split_message_to_sentences(message):
    sentence_pattern = r'(?<=[.!?]) +'
    sentences = re.split(sentence_pattern, message)
    sentences = [sentence.strip() for sentence in re.split(sentence_pattern, message) if sentence.strip()]
    if vars.verbose_tts:
        print(sentences)
    return sentences

def remove_code_snippets(string):
    pattern = r'```[\s\S]*?```'
    clean_text = re.sub(pattern, '', string)
    return clean_text

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
                speaker = messages[0]['speaker']
                text = messages[0]['text']
                timestamp = messages[0]['timestamp']

                # Create a message dictionary for the single message
                message = {
                    'speaker': speaker,
                    'text': text,
                    'timestamp': timestamp
                }

                # Append the single message entry to your list variable
                token_length = get_token_count(build_message_title(message[speaker], message[timestamp]) + build_message_body(message[text]))
                if token_budget >= token_length:  
                    message_list.append(message)
                token_budget = token_budget - token_length
            else:
                # Assuming there are always two messages when there's more than one
                for i in range(0, len(messages), 2):
                    speaker1 = messages[i]['speaker']
                    text1 = messages[i]['text']
                    timestamp1 = messages[i]['timestamp']
                    token_length1 = get_token_count(build_message_title(speaker1, timestamp1) + build_message_body(text1))
                    
                    speaker2 = messages[i + 1]['speaker']
                    text2 = messages[i + 1]['text']
                    timestamp2 = messages[i + 1]['timestamp']
                    token_length2 = get_token_count(build_message_title(speaker2, timestamp2) + build_message_body(text2))
                    
                    # Create message dictionaries for both pairs
                    
                    token_length = token_length1 + token_length2
                    if token_budget >= token_length:                      
                        message = {
                            'speaker': speaker1,
                            'text': text1,
                            'timestamp': timestamp1
                        }
                        message_list.append(message)
                        
                        message = {
                            'speaker': speaker2,
                            'text': text2,
                            'timestamp': timestamp2
                        }
                        message_list.append(message)
                    token_budget = token_budget - token_length

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
    # Define a regular expression pattern for smileys
    smiley_pattern = re.compile(r"(:\)|:\(|;\)|:D|:P|:\||B\)|:-\*|:-O)")    
    text_in_asterisks_pattern = re.compile(r'\*([^*]+)\*')
    text_in_parentheses_pattern = re.compile(r'\(([^)]+)\)')
    hashtag_pattern = re.compile(r'#\w+')
    http_pattern = re.compile(r'https?://\S+')
    # Define a regular expression pattern to match consecutive capital letters
    capital_letters_pattern = re.compile(r'(?<=[a-z])(?=[A-Z])')

    # Remove emojis, text in asterisks, and hashtags from the input text
    filtered_text = emoji_pattern.sub('', input_text)
    filtered_text = text_in_asterisks_pattern.sub('', filtered_text)
    filtered_text = text_in_parentheses_pattern.sub('', filtered_text)
    filtered_text = hashtag_pattern.sub('', filtered_text)
    filtered_text = http_pattern.sub('', filtered_text)
    filtered_text = smiley_pattern.sub('-', filtered_text)
    filtered_text = capital_letters_pattern.sub(' ', filtered_text)
    
    # Replace backticks with single quotes
    filtered_text = filtered_text.replace("`", "\'")
    filtered_text = filtered_text.replace("`a", "'t")
    filtered_text = filtered_text.replace("```", "")
    # Replace ellipsis with full stops
    filtered_text = filtered_text.replace("…", "...")
    # Remove single asterisks
    filtered_text = filtered_text.replace("*", "")
    
    return filtered_text

# AUDIO    
def play_audio(data, fs):
    sd.play(data, fs, device=vars.AUDIO_OUTPUT_DEVICE_ID)
    sd.wait()
    
# LLM PERSONA
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
    if selected_persona == vars.happy_mood:
        if vars.verbose_mood:
            print(Fore.CYAN + f"({vars.ai_name} is happy)\n" + Style.RESET_ALL)
        vars.llm_temperature = 0.4
    if selected_persona == vars.sad_mood:
        if vars.verbose_mood:
            print(Fore.CYAN + f"({vars.ai_name} is sad)\n" + Style.RESET_ALL)
        vars.llm_temperature = 0.1
    if selected_persona == vars.angry_mood:
        if vars.verbose_mood:
            print(Fore.CYAN + f"({vars.ai_name} is angry)\n" + Style.RESET_ALL)
        vars.llm_temperature = 0.5
    if selected_persona == vars.horny_mood:
        if vars.verbose_mood:
            print(Fore.CYAN + f"({vars.ai_name} is aroused)\n" + Style.RESET_ALL)
        vars.llm_temperature = 0.4
    if selected_persona == vars.bored_mood:
        if vars.verbose_mood:
            print(Fore.CYAN + f"({vars.ai_name} is bored)\n" + Style.RESET_ALL)
        vars.llm_temperature = 0.2
    if selected_persona == vars.neutral_mood:
        if vars.verbose_mood:
            print(Fore.CYAN + f"({vars.ai_name} is neutral)\n" + Style.RESET_ALL)
        vars.llm_temperature = 0.3
        
    if vars.verbose_mood:
        print(Fore.CYAN + f"LLM_TEMPERATURE: {vars.llm_temperature}" + Style.RESET_ALL)
        
    vars.active_mood = selected_persona

# LLM PROMPT 
def build_message_title(speaker, timestamp):
    title = f"{speaker} ({timestamp})\n"
    return title
    
def build_message_body(text):
    body = f"{text}\n\n"
    return body

def construct_message(speaker, text, timestamp):
    message = build_message_title(speaker, timestamp) + build_message_body(text)
    return message

def build_title_for_LLM_prompt():
    title = f'(Current Date: {get_current_date()})\n'
    return title

def build_body_for_LLM_prompt():
    body = vars.persona + vars.active_mood + vars.rules + vars.instructions + populate_history() + vars.between_messages + build_message_title(vars.ai_name, get_current_time()) + "\n"
    return body

def construct_prompt_for_LLM():
    prompt = build_title_for_LLM_prompt() + build_body_for_LLM_prompt()
    return prompt

# LLM HISTORY
def populate_history():
    temp_history = ""
    if vars.history_old != []:
        temp_history = temp_history + 'YOUR MEMORIES FROM A OLD CONVERSATION:\n\n'
    
        for entry in vars.history_old:
            temp_history = temp_history + build_message_title(entry['speaker'], entry['timestamp']) + build_message_body(entry['text'])
        
    if vars.history_recent != []:
        temp_history = temp_history + 'YOUR MEMORIES FROM A RECENT CONVERSATION:\n\n'
    
        for entry in vars.history_recent:
            temp_history = temp_history + build_message_title(entry['speaker'], entry['timestamp']) + build_message_body(entry['text'])
                
    if vars.history_current != []:
        temp_history = temp_history + 'YOUR MEMORIES FROM THE CONVERSATION TODAY:\n\n'
    
        for entry in vars.history_current:
            temp_history = temp_history + build_message_title(entry['speaker'], entry['timestamp']) + build_message_body(entry['text'])
    
    return temp_history

def trim_chat_history():
    total_tokens = get_token_count(construct_prompt_for_LLM())

    while total_tokens >= vars.llm_n_ctx:
        last_entry_tokens = vars.history_current[0]['token_length']
        vars.history_current.pop()
        total_tokens -= last_entry_tokens

# LLM SENTIMENT ANALYSIS    
def sentiment_calculation(message):
    if message != "" and message != " ":
        
        if vars.verbose_mood:
            print(Fore.CYAN + f"AI SENTIMENT BEFORE: {vars.llm_mood_score}" + Style.RESET_ALL)
            
        for sentence in split_message_to_sentences(message):
            sentiment = classifier_sentiment(sentence)
            sentiment_strength = 0
            if sentiment[0]['label'] == "positive":
                sentiment_strength = abs(sentiment[0]['score'] * random.gauss(0.2, 0.5))
            if sentiment[0]['label'] == "neutral":
                sentiment_strength = abs(sentiment[0]['score'] / 2 * random.gauss(0.3, 0.6))
            if sentiment[0]['label'] == "negative":
                sentiment_strength = -(abs(sentiment[0]['score'] * random.gauss(0.2, 0.5)))   
                             
            vars.llm_mood_score = vars.llm_mood_score + sentiment_strength    
            
            if vars.verbose_mood:
                print(Fore.CYAN + f"CONVERSATION SENTIMENT: {sentiment_strength} | MOOD: {sentiment[0]['label']}" + Style.RESET_ALL)
        
        if vars.llm_mood_score > 5:
            vars.llm_mood_score = 5
        if vars.llm_mood_score <= 5 and vars.llm_mood_score > 4.5:
            vars.active_mood = random.choice([vars.happy_mood,vars.horny_mood,vars.neutral_mood,vars.bored_mood])
        if vars.llm_mood_score <= 4.5 and vars.llm_mood_score > 3:
            vars.active_mood = random.choice([vars.happy_mood,vars.neutral_mood,vars.bored_mood])
        if vars.llm_mood_score <= 3 and vars.llm_mood_score > 1.5:
            vars.active_mood = random.choice([vars.happy_mood,vars.neutral_mood])
        if vars.llm_mood_score <= 1.5 and vars.llm_mood_score > -1.5:
            vars.active_mood = random.choice([vars.happy_mood,vars.neutral_mood,vars.bored_mood])
        if vars.llm_mood_score <= -1.5 and vars.llm_mood_score > -3:
            vars.active_mood = random.choice([vars.neutral_mood,vars.bored_mood])
        if vars.llm_mood_score <= -3 and vars.llm_mood_score > -4.5:
            vars.active_mood = random.choice([vars.sad_mood,vars.neutral_mood,vars.bored_mood])
        if vars.llm_mood_score <= -4.5 and vars.llm_mood_score > -5:
            vars.active_mood = random.choice([vars.sad_mood,vars.angry_mood,vars.neutral_mood,vars.bored_mood])
        if vars.llm_mood_score < -5:
            vars.llm_mood_score = -5

        if vars.verbose_mood:
            print(Fore.CYAN + f"AI SENTIMENT AFTER: {vars.llm_mood_score}" + Style.RESET_ALL)
        
    current_time = time.time()
    time_difference = current_time - vars.persona_saved_time
    if time_difference > vars.persona_current_change_time:
        swap_persona()
        vars.persona_saved_time = time.time()
        vars.persona_current_change_time = random.randint(vars.persona_min_change_time, vars.persona_max_change_time)


# LLM MEMORY
def write_to_longterm_memory(sender, message):  
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
                    "token": get_token_count(f"{sender}: {message}"),
                    "timestamp": f"{get_current_time()}, {get_current_date()}"
                }
            ]
        })
    else:
        # Append to the existing message block
        memory[-1]['message'].append({
            "speaker": sender,
            "text": message,
            "token": get_token_count(f"{sender}: {message}"),
            "timestamp": f"{get_current_time()}, {get_current_date()}"
        })
    
    # Write the updated chat history back to the JSON file
    with open(generate_file_path("json"), 'w', encoding='utf-8') as json_file:
        json.dump(memory, json_file, indent=4)

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

    # Select one random file from the rest and recent
    if rest_files:
        random_rest_file = random.choice(rest_files)
    if recent_files:
        random_recent_file = random.choice(recent_files)

    # Check available Token count
    token_used = get_token_count(construct_prompt_for_LLM() + vars.instructions_init + f"{vars.ai_name}:")
    token_budget = vars.llm_n_ctx - token_used
    today_budget = (token_budget * 80) / 100
    recent_budget = (token_budget * 15) / 100
    rest_budget = token_budget - today_budget - recent_budget
    while today_budget + recent_budget + rest_budget > token_budget:
        today_budget -= 1

    # Construct file paths if needed
    if rest_files:
        mem = memory_to_history(os.path.join(vars.directory_text, random_rest_file), rest_budget)
        vars.history_old.extend(mem)
    if recent_files:
        mem = memory_to_history(os.path.join(vars.directory_text, random_recent_file), recent_budget)
        vars.history_recent.extend(mem)
    if today_file:
        mem = memory_to_history(os.path.join(vars.directory_text, today_file), today_budget)
        vars.history_current.extend(mem)
        
    trim_chat_history()
   
# COMMANDS
def check_for_keywords_from_list(word_list, message):
    message_lower_cleaned = re.sub(r'[^a-zA-Z\s]', '', message.lower())
    word_counts = {}  # Dictionary to store word counts
    word_list_lower = [word.lower() for word in word_list]
    for word in word_list_lower:
        count = message_lower_cleaned.count(word.lower())
        if count > 0:
            word_counts[word] = count
    if word_counts:
        return word_counts
    else:
        return None

# PROCESSES
def gather_pids():
    vars.init_pids = psutil.pids()

def close_pids(pid_list, search_term):
    gather_pids()
    find_pids(pid_list, search_term)
    for pid in pid_list:
        if psutil.pid_exists(pid):
            try:
                # Terminate the process
                process = psutil.Process(pid)
                process.terminate()
                if vars.verbose_commands:
                    print(f"Process with PID {pid} has been terminated.")
            except psutil.NoSuchProcess:
                if vars.verbose_commands:
                    print(f"No process found with PID {pid}.")
        else:
            if vars.verbose_commands:
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
    if isinstance(search_term, str):
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

        # Clear the external list and extend it with the matching PIDs
        target_list.clear()
        target_list.extend(matching_pids)
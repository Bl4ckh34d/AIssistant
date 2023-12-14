import datetime, time, llama_cpp, random, re, json, os, psutil, win32gui, win32con, win32process, pyautogui, subprocess, pyaudio, time
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
    print("====================================================================")
    print(Fore.MAGENTA + "\n     _      ___               _         _                     _   ")
    print("    / \    |_ _|  ___   ___  (_)  ___  | |_    __ _   _ __   | |_ ")
    print("   / _ \    | |  / __| / __| | | / __| | __|  / _` | | '_ \  | __|")
    print("  / ___ \   | |  \__ \ \__ \ | | \__ \ | |_  | (_| | | | | | | |_ ")
    print(" /_/   \_\ |___| |___/ |___/ |_| |___/  \__|  \__,_| |_| |_|  \__|\n" + Style.RESET_ALL)
    print("YOUR " + Fore.MAGENTA + "TOXIC" + Style.RESET_ALL + "AND" + Fore.MAGENTA + "USELESS" + Style.RESET_ALL + " AI ASSISTANT - " + Fore.MAGENTA + "BETTER" + Style.RESET_ALL + " THAN HAVING " + Fore.MAGENTA + "NO FRIENDS" + Style.RESET_ALL)
    print()
    print("====================================================================")
    print()
    user_name = input("Enter your " + Fore.YELLOW + "NAME" + Style.RESET_ALL + ": ")
    if user_name != "" and user_name != " ":
        vars.user_name = user_name
    else:
        print(Fore.YELLOW + "No input" + Style.RESET_ALL + ". Setting standard name (" + Fore.YELLOW + f"{vars.user_name}" + Style.RESET_ALL + ").")
    print()
    
def setup_user_gender():
    print("Select your " + Fore.YELLOW + "GENDER" + Style.RESET_ALL + ". Currently only male or female are supported.")
    user_gender = input("Enter '1' for " + Fore.YELLOW + "male" + Style.RESET_ALL + " or '2' for " + Fore.YELLOW + "female" + Style.RESET_ALL + ": ")
    if user_gender == "1":
        vars.user_gender = 'male'
    elif user_gender == "2":
        vars.user_gender = 'female'
    else:
        print(Fore.YELLOW + "Invalid input" + Style.RESET_ALL + ". Resorting to standard setting (" + Fore.YELLOW + f"{vars.user_gender}" + Style.RESET_ALL + ")")
    print()
    
def setup_ai_name():
    ai_name = input("Enter the " + Fore.MAGENTA + "NAME" + Style.RESET_ALL + " of your AIssistant: ")
    if ai_name != "" and ai_name != " ":
        vars.ai_name = ai_name
    else:
        print(Fore.MAGENTA + "Invalid input" + Style.RESET_ALL + ". Resorting to standard setting (" + Fore.MAGENTA + f"{vars.ai_name}" + Style.RESET_ALL + ")")
    print()
    
def setup_ai_gender():
    print("Select the " + Fore.MAGENTA + "GENDER" + Style.RESET_ALL + " of your AIssistant. Currently only male or female are supported.")
    ai_gender = input("Enter '1' for " + Fore.MAGENTA + "male" + Style.RESET_ALL + " or '2' for " + Fore.MAGENTA + "female" + Style.RESET_ALL + ": ")
    if ai_gender == "1":
        vars.ai_gender = 'male'
    elif ai_gender == "2":
        vars.ai_gender = 'female'
    else:
        print(Fore.MAGENTA + "Invalid input" + Style.RESET_ALL + ". Resorting to standard setting (" + Fore.MAGENTA + f"{vars.ai_gender}" + Style.RESET_ALL + ")")
        time.sleep(1)
    print()
    #subprocess.call('cls', shell=True)
    
def setup_audio_input():
    print("====================================================================")
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
        print(Fore.MAGENTA + "Invalid input" + Style.RESET_ALL + ". Setting Standard Audio Input Device (" + Fore.MAGENTA + f"{vars.AUDIO_INPUT_DEVICE_ID}" + Style.RESET_ALL + ").")
    
    print()
    #subprocess.call('cls', shell=True)
    
def setup_audio_output():
    print("====================================================================")
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
        print(Fore.MAGENTA + "Invalid input" + Style.RESET_ALL + ". Setting Standard Audio Output Device (" + Fore.MAGENTA + f"{vars.AUDIO_OUTPUT_DEVICE_ID}" + Style.RESET_ALL + ").")
    
    print()
    #subprocess.call('cls', shell=True)

def show_instructions():
    print("====================================================================")
    print()
    print("If you wish to give the AIssistant a command,")
    print("say '" + Fore.MAGENTA + "I command you to..." + Style.RESET_ALL + "' followed by your command.")
    print()
    print("Currently valid commands are: ")
    print(Fore.MAGENTA + "  AGAIN" + Style.RESET_ALL + " will perform the last performed action once more")
    print(Fore.MAGENTA + "  OPEN" + Style.RESET_ALL + " followed by a window/program name or new folder/browser tab")
    print(Fore.MAGENTA + "  CLOSE" + Style.RESET_ALL + " followed by a window/program name or new folder/browser tab")
    print(Fore.MAGENTA + "  REFRESH" + Style.RESET_ALL + " will press F5")
    print(Fore.MAGENTA + "  GO BACK" + Style.RESET_ALL + " + " + Fore.MAGENTA + "TAB/BROWSER" + Style.RESET_ALL + " will press CTRL + SHIFT + TAB")
    print(Fore.MAGENTA + "  SCROLL" + Style.RESET_ALL + " + " + Fore.MAGENTA + "UP/DOWN" + Style.RESET_ALL + " will scroll up or down")
    print(Fore.MAGENTA + "  GO TO" + Style.RESET_ALL + " + " + Fore.MAGENTA + "window/program name" + Style.RESET_ALL + " will try to navigate to that window if already open")
    print(Fore.MAGENTA + "  SWITCH" + Style.RESET_ALL + " + " + Fore.MAGENTA + "window/tab" + Style.RESET_ALL + " will press CTRL + TAB or ALT + TAB respectively")
    print(Fore.MAGENTA + "  MINIMIZE" + Style.RESET_ALL + " will press WIN + DOWN")
    print(Fore.MAGENTA + "  MAXIMIZE" + Style.RESET_ALL + " will press WIN + UP")
    print()
    print("For more info like what programs and folder locations are currently supported,")
    print("have a look at " + Fore.MAGENTA + "commands.py" + Style.RESET_ALL + " and " + Fore.MAGENTA + "command_list.py" + Style.RESET_ALL + " yourself.")
    print()
    print()
    #subprocess.call('cls', shell=True)
    

# UTILITY
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
    chunk_pattern = r'[.!?;–—\'"\u2026\u2014\n](?=\s|$)' #r'(?<=[.!?:—;](?!\w))+'
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

def extract_date_from_filename(filename):
    date_str = filename.split('_')[1].split('.')[0]
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def write_to_file(sender, message, timestamp):
    with open(generate_file_path("txt"), 'a', encoding="utf-8") as file:
        file.write(f"{construct_message(sender, message, timestamp)}")
        
def write_to_current_chat_history(sender, text):
    
    if sender == vars.user_name:
        role = 'user'
    elif sender == vars.ai_name:
        role = 'assistant'
    else:
        role = 'system'
        
    message = {
        'role': role,
        'speaker': sender,
        'text': text,
        "token": get_token_count(f"{sender}: {text}"),
        'timestamp': f"{get_current_time()}"
    }
    
    vars.history_current.append(message)

def json_to_current_chat_history(json_f, token_budget):
    messages = []

    # Read the JSON file
    with open(json_f, 'r') as json_file:
        data = json.load(json_file)
                 
    for entry in data:
        if token_budget > 0:

            messages = entry['message']

            role =  messages[0]['role']
            speaker = messages[0]['speaker']
            text = messages[0]['text']
            token = messages[0]['token']
            timestamp = messages[0]['timestamp']

            # Create a message dictionary for the message
            message = {
                'role': role,
                'speaker': speaker,
                'text': text,
                'token': token,
                'timestamp': timestamp
            }

            # Append message entry to messages
            token_length = get_token_count(build_message_title(speaker, timestamp) + build_message_body(text))
            if token_budget >= token_length:  
                messages.append(message)
            token_budget = token_budget - token_length

    return messages

def replace_acronym(match):
    
    phonetic_mapping = {
        'A': 'aigh ',
        'B': 'bee ',
        'C': 'see ',
        'D': 'dee ',
        'E': 'eeh ',
        'F': 'eff ',
        'G': 'gee ',
        'H': 'age ',
        'I': 'aye ',
        'J': 'jay ',
        'K': 'kay ',
        'L': 'el ',
        'M': 'em ',
        'N': 'en ',
        'O': 'ou ',
        'P': 'pee ',
        'Q': 'queue ',
        'R': 'ar ',
        'S': 'as ',
        'T': 'tee ',
        'U': 'you ',
        'V': 'vee ',
        'W': 'doubleyou ',
        'X': 'eggs ',
        'Y': 'why ',
        'Z': 'zett ',
        'a': 'aigh ',
        'b': 'bee ',
        'c': 'see ',
        'd': 'dee ',
        'e': 'eeh ',
        'f': 'eff ',
        'g': 'gee ',
        'h': 'age ',
        'i': 'aye ',
        'j': 'jay ',
        'k': 'kay ',
        'l': 'el ',
        'm': 'em ',
        'n': 'en ',
        'o': 'ou ',
        'p': 'pee ',
        'q': 'queue ',
        'r': 'ar ',
        's': 'as ',
        't': 'tee ',
        'u': 'you ',
        'v': 'vee ',
        'w': 'doubleyou ',
        'x': 'eggs ',
        'y': 'why ',
        'z': 'zett ',
        '0': 'zero ',
        '1': 'one ',
        '2': 'two ',
        '3': 'three ',
        '4': 'four ',
        '5': 'five ',
        '6': 'six ',
        '7': 'seven ',
        '8': 'eight ',
        '9': 'nine ',
        '&': 'and '
    }
    
    acronym = match.group(0)
    return ''.join(phonetic_mapping.get(char, char) for char in acronym)

def replace_float(match):
    number = match.group()
    if 'E' in number or 'e' in number:
        parts = re.split(r'[Ee]', number)
        integer_part = parts[0] + ' point ' + parts[1].replace('+', ' times ten to the power of ') + ' '

        return integer_part

    parts = number.split('.')
    integer_part = parts[0] + ' point '

    # Spacing out the fractional part after the dot
    fractional_part = ' '.join(parts[1]) if len(parts) > 1 else ''
    spaced_fractional = ' '.join(fractional_part) + ' ' if fractional_part else ''

    return integer_part + spaced_fractional

def replace_math_symbols(match):
    replacements = {
        '-': ' minus ',
        '+': ' plus ',
        '*': ' multiplied by ',
        '/': ' divided by ',
        '^': ' raised to ',
        '=': ' equals ',
        '≠': ' not equal to ',
        '>': ' greater than ',
        '<': ' less than ',
        '≥': ' greater than or equal to ',
        '≤': ' less than or equal to ',
        '√': ' square root of ',
        'sqrt': ' square root of ',
        'Sqrt': ' square root of ',
        '±': ' plus or minus ',
        '%': ' percent ',
        '∞': ' infinity ',
        '°': ' degrees ',
        '∑': ' sum of ',
        '∏': ' product of ',
        '∫': ' integral of ',
        '≈': ' approximately equal to ',
        '∝': ' proportional to ',
        '∀': ' for all ',
        '∃': ' there exists ',
        '∈': ' belongs to ',
        '∉': ' does not belong to ',
        '∅': ' empty set ',
        '²': ' squared ',
        '³': ' cubed ',
        'mc': 'M C ',
        'mc^2': 'M C squared'
    }
    math_symbol = match.group()
    for symbol, replacement in replacements.items():
        math_symbol = math_symbol.replace(symbol, replacement)
    return math_symbol

def replace_numbers(match):
    number_words = {
        '1': 'first',
        '2': 'second',
        '3': 'third',
        '4': 'fourth',
        '5': 'fifth',
        '6': 'sixth',
        '7': 'seventh',
        '8': 'eighth',
        '9': 'ninth',
        '10': 'tenth',
        '11': 'eleventh',
        '12': 'twelfth',
        '13': 'thirteenth',
        '14': 'fourteenth',
        '15': 'fifteenth',
        '16': 'sixteenth',
        '17': 'seventeenth',
        '18': 'eighteenth',
        '19': 'nineteenth',
        '20': 'twentieth'
    }
    number = match.group().strip('. \n\r')  # Strip extra characters
    return number_words[number] + '. '

def replace_greek_alphabet(match):
    replacements = {
        'Α': ' Uppercase Alpha ',
        '\u0391': ' Uppercase Alpha ',
        'α': ' Lowercase Alpha ',
        '\u03B1': ' Lowercase Alpha ',
        'Β': ' Uppercase Beta ',
        '\u0392': ' Uppercase Beta ',
        'β': ' Lowercase Beta ',
        '\u03B2': ' Lowercase Beta ',
        'Γ': ' Uppercase Gamma ',
        '\u0393': ' Uppercase Gamma ',
        'γ': ' Lowercase Gamma ',
        '\u03B3': ' Lowercase Gamma ',
        'Δ': ' Uppercase Delta ',
        '\u0394': ' Uppercase Delta ',
        'δ': ' Lowercase Delta ',
        '\u03B4': ' Lowercase Delta ',
        'Ε': ' Uppercase Epsilon ',
        '\u0395': ' Uppercase Epsilon ',
        'ε': ' Lowercase Epsilon ',
        '\u03B5': ' Lowercase Epsilon ',
        'Ζ': ' Uppercase Zeta ',
        '\u0396': ' Uppercase Zeta ',
        'ζ': ' Lowercase Zeta ',
        '\u03B6': ' Lowercase Zeta ',
        'Η': ' Uppercase Eta ',
        '\u0397': ' Uppercase Eta ',
        'η': ' Lowercase Eta ',
        '\u03B7': ' Lowercase Eta ',
        'Θ': ' Uppercase Theta ',
        '\u0398': ' Uppercase Theta ',
        'θ': ' Lowercase Theta ',
        '\u03B8': ' Lowercase Theta ',
        'Ι': ' Uppercase Iota ',
        '\u0399': ' Uppercase Iota ',
        'ι': ' Lowercase Iota ',
        '\u03B9': ' Lowercase Iota ',
        'Κ': ' Uppercase Kappa ',
        '\u039A': ' Uppercase Kappa ',
        'κ': ' Lowercase Kappa ',
        '\u03BA': ' Lowercase Kappa ',
        'Λ': ' Uppercase Lambda ',
        '\u039B': ' Uppercase Lambda ',
        'λ': ' Lowercase Lambda ',
        '\u03BB': ' Lowercase Lambda ',
        'Μ': ' Uppercase Mu ',
        '\u039C': ' Uppercase Mu ',
        'μ': ' Lowercase Mu ',
        '\u03BC': ' Lowercase Mu ',
        'Ν': ' Uppercase Nu ',
        '\u039D': ' Uppercase Nu ',
        'ν': ' Lowercase Nu ',
        '\u03BD': ' Lowercase Nu ',
        'Ξ': ' Uppercase Xi ',
        '\u039E': ' Uppercase Xi ',
        'ξ': ' Lowercase Xi ',
        '\u03BE': ' Lowercase Xi ',
        'Ο': ' Uppercase Omicron ',
        '\u039F': ' Uppercase Omicron ',
        'ο': ' Lowercase Omicron ',
        '\u03BF': ' Lowercase Omicron ',
        'Π': ' Uppercase Pi ',
        '\u03A0': ' Uppercase Pi ',
        'π': ' Lowercase Pi ',
        '\u03C0': ' Lowercase Pi ',
        'Ρ': ' Uppercase Rho ',
        '\u03A1': ' Uppercase Rho ',
        'ρ': ' Lowercase Rho ',
        '\u03C1': ' Lowercase Rho ',
        'Σ': ' Uppercase Sigma ',
        '\u03A3': ' Uppercase Sigma ',
        'σ': ' Lowercase Sigma ',
        '\u03C3': ' Lowercase Sigma ',
        'Τ': ' Uppercase Tau ',
        '\u03A4': ' Uppercase Tau ',
        'τ': ' Lowercase Tau ',
        '\u03C4': ' Lowercase Tau ',
        'Υ': ' Uppercase Upsilon ',
        '\u03A5': ' Uppercase Upsilon ',
        'υ': ' Lowercase Upsilon ',
        '\u03C5': ' Lowercase Upsilon ',
        'Φ': ' Uppercase Phi ',
        '\u03A6': ' Uppercase Phi ',
        'φ': ' Lowercase Phi ',
        '\u03C6': ' Lowercase Phi ',
        'Χ': ' Uppercase Chi ',
        '\u03A7': ' Uppercase Chi ',
        'χ': ' Lowercase Chi ',
        '\u03C7': ' Lowercase Chi ',
        'Ψ': ' Uppercase Psi ',
        '\u03A8': ' Uppercase Psi ',
        'ψ': ' Lowercase Psi ',
        '\u03C8': ' Lowercase Psi ',
        'Ω': ' Uppercase Omega ',
        '\u03A9': ' Uppercase Omega ',
        'ω': ' Lowercase Omega ',
        '\u03C9': ' Lowercase Omega '
    }
    greek_alphabet = match.group()
    for symbol, replacement in replacements.items():
        greek_alphabet = greek_alphabet.replace(symbol, replacement)
    return greek_alphabet

def filter_text(input_text):
    everything_pattern = re.compile(r'[^a-zA-Z\s\d.,?!;:\'"&%/\\(){}\[\]=$§"\'+~*#<>|^°-]')
    greek_pattern = re.compile(r'[\u0391-\u03A9\u03B1-\u03C9]|[Α-Ωα-ω]')
    float_pattern = re.compile(r'\b\d+(\.\d+)?[Ee][+-]?\d+\b|\b\d+\.\d+\b')
    math_pattern = re.compile(r'mc^2|[-+*/^=≠><≥≤√±%∞°∑∏∫≈∝∀∃∈∉∅]|sqrt|Sqrt|²|³|mc')
    numbered_pattern = re.compile(r'(?:^|\n|\s+)(?:[1-9]|1[0-9]|20)\. ')
    smiley_pattern = re.compile(r"(\s:\)|\s:\(|\s;\)|\s:D|\s:P|\s:\||\sB\)|\s:-\*|\s:-O|\s:\/)")
    acronym_pattern = re.compile(r'\b(?:[A-Z0-9&]*[A-Z]){2,3}[A-Z0-9&]*\b|\b(?:[A-Z0-9&]*[A-Z]){3}[A-Z0-9&]*\b')
    # Modified acronym pattern excluding the specific acronym
    modified_acronym_pattern = re.compile(
        rf'\b(?!(?:{vars.ai_name}))' + acronym_pattern.pattern
    )
    and_pattern = re.compile(r'&amp;')
    ellipsis_pattern = re.compile(r'\.{2,}|\u2026')
    multiple_hashtag_pattern = re.compile(r'\#{2,}')
    hashtag_pattern = re.compile(r'[\s.]?\#')
    bracket_pattern = re.compile(r'[\s.]?[\(\)]')
    backtick_pattern = re.compile(r'`(\s*[^`]|[^`])')
    asterisk_pattern = re.compile(r'\*+')
    heart_pattern = re.compile(r'\s*<3+\s*')
    br_pattern = re.compile(r'\s*<br>\s*')
    eos_token_pattern = re.compile(r'\s*' + vars.eos_token + r'\s*')
    comma_after_punctuation_pattern = re.compile(r'(?<=[.!?;,:])\s*,')
    for_example_pattern = re.compile(r'\b(e\.g\.)\b')
    id_est_pattern = re.compile(r'\b(i\.e\.)\b')
    
    filtered_text = greek_pattern.sub(replace_greek_alphabet, input_text)
    filtered_text = float_pattern.sub(replace_float, filtered_text)
    filtered_text = math_pattern.sub(replace_math_symbols, filtered_text)
    filtered_text = numbered_pattern.sub(replace_numbers, filtered_text)
    filtered_text = smiley_pattern.sub('', filtered_text)
    # Check if the input consists solely of acronyms
    if modified_acronym_pattern.fullmatch(filtered_text):
        return ' '.join(replace_acronym(match) for match in modified_acronym_pattern.finditer(filtered_text))
    else:
        filtered_text = modified_acronym_pattern.sub(replace_acronym, filtered_text)
    filtered_text = and_pattern.sub('&', filtered_text)
    filtered_text = ellipsis_pattern.sub('.', filtered_text)
    filtered_text = multiple_hashtag_pattern.sub('', filtered_text)
    filtered_text = hashtag_pattern.sub('Hashtag', filtered_text)
    filtered_text = bracket_pattern.sub('', filtered_text)
    filtered_text = backtick_pattern.sub("'", filtered_text)
    filtered_text = asterisk_pattern.sub('', filtered_text)
    filtered_text = heart_pattern.sub("I love you!", filtered_text)
    filtered_text = br_pattern.sub("\n", filtered_text)
    filtered_text = eos_token_pattern.sub("\n", filtered_text)
    filtered_text = comma_after_punctuation_pattern.sub('', filtered_text)
    filtered_text = for_example_pattern.sub('for example', filtered_text)
    filtered_text = id_est_pattern.sub('that is', filtered_text)
    
    filtered_text = everything_pattern.sub('', filtered_text)
    
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

def construct_message_with_objects(speaker, text, timestamp):
    message = [
            {
                'role':'system',
                'content':f'{speaker} ({timestamp})\n'
            },
            {
                'role':f'{speaker}',
                'content':f'{text}\n\n'
            }        
        ]
    return message

def build_system_prompt():
    system_prompt = vars.persona + vars.active_mood + vars.rules + vars.instructions
    return system_prompt

def build_system_prompt_with_objects():
    message = [
        {
            'role':'system',
            'content':vars.persona + vars.active_mood + vars.rules + vars.instructions
        }
    ]
    return message

def build_user_prompt():
    user_prompt = populate_history() + "\n" + build_message_title(vars.ai_name, get_current_time()) + "\n"
    return user_prompt

def build_user_prompt_with_objects():
    messages = []
    message = [
        {
            'role':'system',
            'content':f'{vars.ai_name} ({get_current_time()})\n'
        }
    ]
    messages.extend(populate_history_with_objects())
    messages.extend(message)
    return messages

# LLM HISTORY
def populate_history():
    temp_history = ""
    if vars.history_old != []:
        temp_history = temp_history + 'Your memories from an old conversation:\n\n'
    
        for entry in vars.history_old:
            temp_history = temp_history + build_message_title(entry['speaker'], entry['timestamp']) + build_message_body(entry['text'])
        
    if vars.history_recent != []:
        temp_history = temp_history + 'Your memories from a recent conversation:\n\n'
    
        for entry in vars.history_recent:
            temp_history = temp_history + build_message_title(entry['speaker'], entry['timestamp']) + build_message_body(entry['text'])
                
    if vars.history_current != []:
        if len(vars.history_current) > 1:
            temp_history = temp_history + 'Your memories from todays conversation:\n\n'
    
        for entry in vars.history_current:
            temp_history = temp_history + build_message_title(entry['speaker'], entry['timestamp']) + build_message_body(entry['text'])
    return temp_history

def populate_history_with_objects():
    temp_history = []
    if vars.history_old != []:
        message = [
            {
                'role':'system',
                'content':'Your memories from an old conversation:\n\n'
            }
        ]
        temp_history.extend(message)
        
        for entry in vars.history_old:
            message = [
                {
                    'role':'system',
                    'content':f'{entry["speaker"]} ({get_current_time()})\n'
                }
            ]
            temp_history.extend(message)
            message = [
                {
                    'role':entry['role'],
                    'content':entry['text']
                }
            ]
            temp_history.extend(message)
            
    if vars.history_recent != []:
        message = [
            {
                'role':'system',
                'content':'Your memories from a recent conversation:\n\n'
            }
        ]
        temp_history.extend(message)
        
        for entry in vars.history_recent:
            message = [
                {
                    'role':'system',
                    'content':f'{entry["speaker"]} ({get_current_time()})\n'
                }
            ]
            temp_history.extend(message)
            message = [
                {
                    'role':entry['role'],
                    'content':entry['text']
                }
            ]
            temp_history.extend(message)
        
    if vars.history_current != []:
        if len(vars.history_current) > 1:
            message = [
                {
                    'role':'system',
                    'content':'Your memories from todays conversation:\n\n'
                }
            ]
            temp_history.extend(message)
        
        for entry in vars.history_current:
            message = [
                {
                    'role':'system',
                    'content':f'{entry["speaker"]} ({get_current_time()})\n'
                }
            ]
            temp_history.extend(message)
            message = [
                {
                    'role':entry['role'],
                    'content':entry['text']
                }
            ]
            temp_history.extend(message)
            
    return temp_history

def trim_chat_history():
    total_tokens = get_token_count(build_system_prompt() + build_user_prompt())

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
def write_to_json(sender, message):  
    # Load existing chat history (if any)
    try:
        with open(generate_file_path("json"), 'r', encoding='utf-8') as json_file:
            memory = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty chat history
        memory = []
        
    if sender == vars.user_name:
        role = 'user'
    elif sender == vars.ai_name:
        role = 'assistant'
    else:
        role = 'system'
        
    # Create a new message block
    memory.append({
        "message": [
            {
                "role": role,
                "speaker": sender,
                "text": message,
                "token": get_token_count(f"{sender}: {message}"),
                "timestamp": f"{get_current_time()}, {get_current_date()}"
            }
        ]
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
    token_used = get_token_count(build_system_prompt() + build_user_prompt())
    token_budget = vars.llm_n_ctx - token_used
    today_budget = (token_budget * 80) / 100
    recent_budget = (token_budget * 15) / 100
    rest_budget = token_budget - today_budget - recent_budget
    while today_budget + recent_budget + rest_budget > token_budget:
        today_budget -= 1

    # Construct file paths if needed
    if rest_files:
        mem = json_to_current_chat_history(os.path.join(vars.directory_text, random_rest_file), rest_budget)
        vars.history_old.extend(mem)
    if recent_files:
        mem = json_to_current_chat_history(os.path.join(vars.directory_text, random_recent_file), recent_budget)
        vars.history_recent.extend(mem)
    if today_file:
        mem = json_to_current_chat_history(os.path.join(vars.directory_text, today_file), today_budget)
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
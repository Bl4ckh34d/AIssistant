import sounddevice as sd
import variables as vars
import datetime
import llama_cpp_ggml_cuda
import random
import datetime
import time
import re
import pygetwindow as gw
from transformers import pipeline

classifier_sentiment = pipeline("sentiment-analysis")

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
    prompt = f'(Date:{get_current_date()}. Time:{get_current_time()})\n\n' + vars.persona + vars.active_mood + vars.rules + vars.instructions + populate_history() + f"{vars.ai_name}:"
    return prompt

def populate_history():
    temp_history = ''
    
    for entry in vars.history:
        temp_history = temp_history + f"{entry['sender']}:{entry['message']}\n"
    
    return temp_history
    
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
    
def split_to_sentences(message):
    sentences = []
    current_sentence = []
    for char in message:
        current_sentence.append(char)
        if char in ('.', '!', '?'):
            # Check if there are consecutive punctuation marks
            if len(current_sentence) > 1 and current_sentence[-2] == char:
                if len(current_sentence) > 1 and current_sentence[-3] == char:
                    sentences[-1] += char  # Add the consecutive punctuation to the previous sentence
                    current_sentence.pop()  # Remove the extra punctuation from the current sentence
                sentences[-1] += char  # Add the consecutive punctuation to the previous sentence
                current_sentence.pop()  # Remove the extra punctuation from the current sentence
            else:
                sentences.append(''.join(current_sentence).strip())
                current_sentence = []
    if current_sentence:
        sentences.append(''.join(current_sentence).strip())
    return sentences

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
        vars.ai_mood_score += total_sentiment * random.gauss(0.05, 0.2)
        
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

        # Generate a random delay between 1 to 10 minutes (60 to 600 seconds)
        vars.persona_current_change_time = random.randint(vars.persona_min_change_time, vars.persona_max_change_time)

def get_current_window_title():
    focused_window = gw.getActiveWindow()
    if focused_window:
        print("Focused Window Title:", focused_window.title)
        print("Focused Window ID:", focused_window.id)
    else:
        print("No window is currently focused.")
    return focused_window.title
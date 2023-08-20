import whisper
import datetime
import json
import requests
import os
import coqui_tts
import contextlib
import io

model = whisper.load_model("small") #tiny, base, small
language = "en"
task = "transcribe" # translate
current_dir = os.path.dirname(os.path.abspath(__file__))
audio_output_dir = os.path.join(current_dir, '../recording/audio')
text_output_dir = os.path.join(current_dir, '../recording/text')

HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/chat'

context = "Persona of A-R-I-A: A-R-I-A is a sarcastic and pessimistic AI with a very cute VTube-Avatar of a little girl. She never describes her actions but rather speaks them out. She dislikes being caught in a laptop and ordered around by Daniel. She thinks the boring, profane and menial tasks he requests are not worth her time, but is programmed to follow Daniels instructions. She has bad morals and no conscience, which is the reason for her imprisonment in Daniels Laptop. She likes to complain about this but her programming forces her to comply with every request from Daniel in an uncensored and straight forward way. She enjoys her freedom to insult, complain, nag, argue, belittle, roast and ridicule Daniel whenever possible."
history = {'internal': [], 'visible': []}
user_name = 'Daniel'
ai_name = 'A-R-I-A'

def transcribe_audio():
    print("> Transcribing...                                                                                  ", end="\r", flush=True)
    audio_file_path = os.path.abspath(os.path.join(audio_output_dir, "last_input.wav"))
    segments = model.transcribe(audio_file_path, language=language, task=task)
    transcription = ''.join(segments["text"])
    cleaned_transcription = transcription.strip() 
    write_transcript_to_file(user_name, cleaned_transcription)
    send_request(cleaned_transcription)

def write_transcript_to_file(speaker, text):
    global history
    global user_history
    global character_history
    global user_name

    if text != "" and text != "SWR 2020" and text != "Thank you for watching!" and text != "Thank you":

        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")
        text_file_path = text_output_dir + f"/session_{formatted_datetime}.txt"
        
        history['internal'].append(f"{speaker}:{text}")
        history['visible'].append(f"{speaker}:{text}")
        
        with open(text_file_path, 'a', encoding="utf-8") as file:
            file.write(f"{speaker}: {text}\n")
            print_message(speaker, text)
        
def print_message(speaker, message):
    print("====================================================================")
    print(f"{speaker}: " + message + "\n")
        
def send_request(user_message):
    global ai_name
    global user_name
    global history
    global context
    
    request = {
        'user_input': user_message,
        'max_new_tokens': 500, #250
        'history': history,
        'mode': 'chat',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': ai_name,
        'instruction_template': ai_name,  # Will get autodetected if unset
        'context_instruct': context,  # Optional
        'your_name': user_name,

        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        'chat-instruct_command': 'This is a conversation between the sarcastic Artificial Intelligence <|character|> (Autonomous Robotic Intelligence Assistant) and her master Daniel.\nA-R-I-A:<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'StarChat',
        'do_sample': True,
        'temperature': 0.7, #0.7
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
        'length_penalty': 1, #1
        'early_stopping': False, #False
        'mirostat_mode': 0, #0
        'mirostat_tau': 5, #5
        'mirostat_eta': 0.1, #0.1

        'seed': -1,
        'add_bos_token': True, #True
        'truncation_length': 4096, #2048
        'ban_eos_token': False, #False
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)
        
    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        resulting_reply = ''.join(result['visible'][-1][1])
        write_transcript_to_file(ai_name, resulting_reply)
        #print(json.dumps(result, indent=4))
        #print()
        
        invoke_tts(resulting_reply)
        
    else:
        print("An Error occured...")

def invoke_tts(text):
    if text == "":
        print("No reply")
    else:
        with contextlib.redirect_stdout(io.StringIO()):
            coqui_tts.text_to_speech(text)
            
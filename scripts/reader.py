import os
import io
import datetime
import contextlib
import soundfile as sf
import sounddevice as sd
from TTS.api import TTS
from multiprocessing import Process, Queue

# Constants
AUDIO_DEVICE_ID_SPEAKERS = 6  # Adjust this as needed
DIRECTORY_AUDIO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../recording/audio')
DIRECTORY_TTS_MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../models/tts')

def initialize_paths():
    tts_model_name = 'tts_models--en--jenny--jenny'
    tts_model_path = os.path.abspath(os.path.join(DIRECTORY_TTS_MODEL, tts_model_name))
    tts_model_file_path = os.path.abspath(os.path.join(tts_model_path, "model.pth"))
    tts_model_config_file_path = os.path.abspath(os.path.join(tts_model_path, "config.json"))
    return tts_model_file_path, tts_model_config_file_path

def load_tts_model(model_path, config_path):
    return TTS(model_path=model_path, config_path=config_path, progress_bar=False).to("cuda")

def main():
    # Initialize TTS model paths
    tts_model_file_path, tts_model_config_file_path = initialize_paths()
    tts = load_tts_model(tts_model_file_path, tts_model_config_file_path)

    input_text = """
Stable Diffusion:

Stable diffusion is a method to create images by slowly changing a starting image in tiny steps. Imagine you have a picture, and you want to transform it into something different. With stable diffusion, you make really small changes to the picture over many steps, like adjusting the colors or shapes bit by bit. This gradual transformation creates new and interesting images.

There are different types of stable diffusion, like guided diffusion and simple diffusion. Guided diffusion means having a specific goal in mind while changing the image, like making it look more like a particular style or object. Simple diffusion doesn't have a specific goal; it's more about letting the image change randomly, which can also produce cool results.
GANs (Generative Adversarial Networks):

Think of GANs like a competition between two artists: one is trying to create fake art, and the other is trying to spot what's fake. But instead of art, they work with images.

One artist, called the "generator," makes fake images and tries to make them look as real as possible. It learns from real images to improve its fakes. The other artist, called the "discriminator," looks at both real and fake images and tries to tell them apart.

As they play this game, both get better: the generator learns to make more realistic fakes, while the discriminator gets better at spotting them. This back-and-forth makes the generator produce images that start to look very real, even though they're not. Eventually, the fakes can be so good that it's hard to tell them apart from real images!

So, in short, stable diffusion changes images gradually, while GANs involve a competition between a creator and a judge to make really convincing fake images.
"""

    sentences = split_to_sentences(input_text)
    audio_queue = Queue()

    playback_process = Process(target=audio_playback_worker, args=(audio_queue, 0))  # Pass 0 as the initial file_counter
    playback_process.start()

    for sentence in sentences:
        if sentence:
            audio_generator(sentence, tts, audio_queue)

    # Signal the playback process to stop after all sentences are played
    audio_queue.put(None)
    playback_process.join()

def create_audio(text, tts, file_counter):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    audio_filename = f"readout_output_{timestamp}_{file_counter}.wav"
    tts_output_file_path = os.path.abspath(os.path.join(DIRECTORY_AUDIO, audio_filename))
    with contextlib.redirect_stdout(io.StringIO()) as fake_stdout:
        tts.tts_to_file(text=text, file_path=tts_output_file_path, gpu=True)
    print(f"SYSTEM: File #{file_counter} created: {audio_filename}")
    return tts_output_file_path

def audio_playback(file_path, file_counter):
    try:
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate)
        print(f"SYSTEM: File #{file_counter} playing: {file_path}")
        sd.wait()
        remove_file(file_path, file_counter)
    except Exception as e:
        print(f"SYSTEM: Error during audio playback of File #{file_counter} ({file_path}): {str(e)}")

def remove_file(file_path, file_counter):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"SYSTEM: File #{file_counter} ({file_path}) deleted.")
    else:
        print(f"SYSTEM: File #{file_counter} ({file_path}) does not exist.")

def split_to_sentences(text):
    sentences = []
    current_sentence = ""
    for word in text.split():
        current_sentence += word + " "
        if word.endswith((' - ', '.', '!', '?', ':', '|')):
            sentences.append(current_sentence.strip())
            current_sentence = ""
    if current_sentence:
        sentences.append(current_sentence.strip())
    return sentences

def audio_generator(sentence, tts, queue):
    global file_counter  # Access the global counter
    file_counter += 1  # Increment the counter
    tts_output_file_path = create_audio(sentence, tts, file_counter)
    queue.put(tts_output_file_path)

def audio_playback_worker(queue, file_counter):
    while True:
        tts_output_file_path = queue.get()
        if tts_output_file_path is None:
            break
        audio_playback(tts_output_file_path, file_counter)

if __name__ == "__main__":
    file_counter = 0  # Initialize the global file counter
    main()
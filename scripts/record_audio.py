import pyaudio
import math
import struct
import wave
import time
import os
import STT

Init_Threshold = 15
Threshold = 20

current_dir = os.path.dirname(os.path.abspath(__file__))
audio_output_dir = os.path.join(current_dir, '../recording/audio')
text_output_dir = os.path.join(current_dir, '../recording/text')

short_normalize = (1.0/32768.0)
pyaudio_format = pyaudio.paInt16
num_channels = 1
hz_rate = 16000
swidth = 2
chunk_size = 1024

timeout_length = 1.5

class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * short_normalize
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio_format,
                                  channels=num_channels,
                                  rate=hz_rate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk_size)

    def record(self):
        rec = []
        current = time.time()
        end = time.time() + timeout_length
        minCounter = 0

        while current <= end:
            data = self.stream.read(chunk_size)
            rms_val = self.rms(data)
            if rms_val >= Threshold:
                end = time.time() + timeout_length
                if minCounter % 2 == 0:
                    altSymbol = "▋"
                else:
                    altSymbol = "█"
                print(f'> Noise detected, recording: {"█" * minCounter + altSymbol}', end='\r', flush=True)
                #print('\n> Noise detected, recording: ', end='', flush=True)
                #print('|', end='', flush=True) # Print a line if threshold is reached
                if minCounter < 38:
                    minCounter += 1
            
            current = time.time()
            rec.append(data)
        #print("") # Move to the next line after recording is done
            
        if minCounter > 3:  # Check if the recording contains more than one chunk
            self.write(b''.join(rec))
        else:
            print("> Discarding recording (Too short)", end='\r', flush=True)
        
    def write(self, recording):
        filename = os.path.join(audio_output_dir, 'last_input.wav')

        wf = wave.open(filename, 'wb')
        wf.setnchannels(num_channels)
        wf.setsampwidth(self.p.get_sample_size(pyaudio_format))
        wf.setframerate(hz_rate)
        wf.writeframes(recording)
        wf.close()

        STT.transcribe_audio()



    def listen(self):
        print('> Speak, when you are ready...')
        while True:
            input = self.stream.read(chunk_size)
            rms_val = self.rms(input)
            if rms_val > Init_Threshold:
                self.record()


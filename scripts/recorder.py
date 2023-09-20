import pyaudio, math, struct, wave, time, os, AI_STT
import variables as vars

class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / vars.S_WIDTH
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * vars.SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=vars.NUM_CHANNELS,
                                  rate=vars.HZ_RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=vars.CHUNK_SIZE)

    def record(self):
        rec = []
        current = time.time()
        end = time.time() + vars.RECORDING_TIMEOUT_BEFORE_STOP
        minCounter = 0

        while current <= end:
            data = self.stream.read(vars.CHUNK_SIZE)
            rms_val = self.rms(data)
            if rms_val >= vars.RECORDING_CONTINUOUS_THRESHOLD:
                end = time.time() + vars.RECORDING_TIMEOUT_BEFORE_STOP
                if minCounter % 2 == 0:
                    altSymbol = "▋"
                else:
                    altSymbol = "█"
                print(f'> Noise detected, recording: {"█" * minCounter + altSymbol}', end='\r', flush=True)
                if minCounter < 38:
                    minCounter += 1
            
            current = time.time()
            rec.append(data)
            
        if minCounter > 3:  # Check if the recording contains more than 3 chunks
            self.write(b''.join(rec))
        else:
            print("> Discarding recording (Too short)", end='\r', flush=True)
        
    def write(self, recording):
        filename = os.path.join(vars.directory_audio, 'last_input.wav')

        wf = wave.open(filename, 'wb')
        wf.setnchannels(vars.NUM_CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(vars.HZ_RATE)
        wf.writeframes(recording)
        wf.close()

        AI_STT.transcribe_audio()

    def listen(self):
        print('> Speak, when you are ready...')
        while True:
            input = self.stream.read(vars.CHUNK_SIZE)
            rms_val = self.rms(input)
            if rms_val > vars.RECORDING_INIT_THRESHOLD:
                self.record()


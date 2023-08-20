import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()

    print("Available Audio Input Devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:
            print(f"ID: {device_info['index']}, Name: {device_info['name']}")

    print("\nAvailable Audio Output Devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxOutputChannels'] > 0:
            print(f"ID: {device_info['index']}, Name: {device_info['name']}")

    p.terminate()

if __name__ == "__main__":
    list_audio_devices()
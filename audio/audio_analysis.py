import sounddevice as sd
import numpy as np

all_devices = sd.query_devices()
device_names = [f"[{i}] {d['name']}" for i, d in enumerate(all_devices) if d['max_input_channels'] > 0]
input_device_indices = [i for i, d in enumerate(all_devices) if d['max_input_channels'] > 0]

current_device_index = 0
stream = None

def initialize_audio(device_index=0, sample_rate=44100, frame_size=1024, mel_bands=1024):
    global stream, current_device_index
    current_device_index = device_index

    def callback(indata, frames, time, status):
        global last_audio_frame
        last_audio_frame = np.copy(indata[:, 0])

    stream = sd.InputStream(
        callback=callback,
        samplerate=sample_rate,
        blocksize=frame_size,
        device=device_index,
        channels=1
    )
    stream.start()

last_audio_frame = np.zeros(1024)

def get_mel_bands():
    return np.abs(np.fft.rfft(last_audio_frame))[:1024]

def switch_audio_device(new_index):
    global stream
    if stream:
        stream.stop()
        stream.close()
    initialize_audio(device_index=new_index)
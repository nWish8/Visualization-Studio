import sounddevice as sd
import numpy as np

all_devices = sd.query_devices()
device_names = [f"[{i}] {d['name']}" for i, d in enumerate(all_devices) if d['max_input_channels'] > 0]
input_device_indices = [i for i, d in enumerate(all_devices) if d['max_input_channels'] > 0]

current_device_index = 0
stream = None

def get_stereo_mix_index():
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        if "Stereo Mix" in device['name'] and device['max_input_channels'] > 0:
            return i
    return None  # fallback if not found

def initialize_audio(sample_rate=44100, frame_size=1024, mel_bands=64):
    device_index = get_stereo_mix_index()

    if device_index is not None:
        print(f"✅ Auto-selected loopback device: {device_index} - {sd.query_devices(device_index)['name']}")
    else:
        print("⚠️ Stereo Mix not found, using default input device")
        device_index = None  # fallback to system default

    stream = sd.InputStream(
        device=device_index,
        channels=1,
        samplerate=sample_rate,
        blocksize=frame_size,
        callback=,
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
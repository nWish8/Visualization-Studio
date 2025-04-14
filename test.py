import sounddevice as sd
import numpy as np

def find_best_input_device(prefer_loopback=True):
    devices = sd.query_devices()
    fallback = None

    for idx, dev in enumerate(devices):
        name = dev['name'].lower()
        if dev['max_input_channels'] > 0:
            if prefer_loopback and ('loopback' in name or 'stereo mix' in name):
                print(f"✅ Selected loopback device: [{idx}] {dev['name']}")
                return idx, int(dev['default_samplerate'])
            elif fallback is None:
                fallback = (idx, int(dev['default_samplerate']))

    print(f"⚠️ No loopback found. Using fallback: [{fallback[0]}] {devices[fallback[0]]['name']}")
    return fallback

def audio_callback(indata, frames, time, status):
    if status:
        print("⚠️", status)
    volume = np.linalg.norm(indata)  # RMS volume
    print(f"🎚 Volume: {volume:.4f}")

# 🔍 Step 1: Find best device and sample rate
device_id, sample_rate = find_best_input_device()

# 🔧 Step 2: Open input stream
stream = sd.InputStream(
    device=device_id,
    samplerate=sample_rate,
    channels=1,
    callback=audio_callback,
    blocksize=512
)

# 🚀 Step 3: Start stream and listen
print(f"\n🎧 Listening on device {device_id} at {sample_rate} Hz...\n")
stream.start()

input("🔊 Play music now. Press ENTER to stop...\n")

stream.stop()
stream.close()

from audio_input import AudioInput
import time

audio = AudioInput(mel_bands=64)
audio.start()

print("🎧 Listening (Mel Mode)...")
try:
    while True:
        volume, spectrum, mel = audio.get_features()
        print(f"Vol: {volume:.4f} | Mel: {mel[:5]}")
        time.sleep(0.1)
except KeyboardInterrupt:
    audio.stop()
    print("🔇 Audio stopped.")

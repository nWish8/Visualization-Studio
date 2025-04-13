import numpy as np
import sounddevice as sd
import librosa

# Audio config
SAMPLE_RATE = 44100
BUFFER_SIZE = 2048
MEL_BANDS = 128

# Shared audio buffer
audio_buffer = np.zeros(BUFFER_SIZE, dtype=np.float32)

# Librosa Mel filter bank (computed once)
mel_filter_bank = librosa.filters.mel(sr=SAMPLE_RATE, n_fft=BUFFER_SIZE, n_mels=MEL_BANDS)

# Audio callback to fill buffer
def audio_callback(indata, frames, time, status):
    global audio_buffer
    if status:
        print(status)
    audio_buffer = np.copy(indata[:, 0])

# Start input stream (run this once on import)
stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE)
stream.start()

# Function to get mel band energy
def get_mel_bands(n_bands=MEL_BANDS):
    global audio_buffer

    # Apply window to reduce artifacts
    windowed = audio_buffer * np.hanning(len(audio_buffer))

    # Compute FFT and power spectrum
    fft = np.abs(np.fft.rfft(windowed))**2

    # Apply Mel filter bank
    mel_spectrum = np.dot(mel_filter_bank, fft[:mel_filter_bank.shape[1]])

    # Normalize and scale
    mel_spectrum = np.log1p(mel_spectrum)
    mel_spectrum = mel_spectrum / np.max(mel_spectrum + 1e-6)

    # Pad or truncate to match grid resolution
    if n_bands < MEL_BANDS:
        return mel_spectrum[:n_bands].astype(np.float32)
    elif n_bands > MEL_BANDS:
        return np.pad(mel_spectrum, (0, n_bands - MEL_BANDS)).astype(np.float32)
    else:
        return mel_spectrum.astype(np.float32)

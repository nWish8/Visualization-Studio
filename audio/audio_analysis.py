import numpy as np
import sounddevice as sd
import librosa
import threading

class AudioAnalyzer:
    def __init__(self, sample_rate=44100, frame_size=1024, mel_bands=64):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.mel_bands = mel_bands
        self.latest_samples = np.zeros(self.frame_size)
        self.latest_mel = np.zeros(self.mel_bands, dtype=np.float32)
        self.lock = threading.Lock()

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            channels=1,
            callback=self.audio_callback
        )

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("[Audio Warning]", status)
        samples = indata[:, 0]  # use first channel for mono input
        with self.lock:
            self.latest_samples = samples.copy()
            # Compute Mel spectrogram on the current chunk
            mel = librosa.feature.melspectrogram(
                y=samples.astype(np.float32),
                sr=self.sample_rate,
                n_fft=self.frame_size,
                n_mels=self.mel_bands,
                fmax=self.sample_rate / 2
            )
            # Convert power spectrogram to decibels, then normalize to [0,1]
            mel_db = librosa.power_to_db(mel, ref=np.max)
            mel_norm = (mel_db - np.min(mel_db)) / (np.max(mel_db) - np.min(mel_db) + 1e-6)
            # Use the latest time slice (last column)
            self.latest_mel = mel_norm[:, -1]

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def get_mel_bands(self):
        with self.lock:
            return self.latest_mel.copy()

# Global analyzer instance for convenience
audio_analyzer = None

def initialize_audio(sample_rate=44100, frame_size=1024, mel_bands=64):
    global audio_analyzer
    audio_analyzer = AudioAnalyzer(sample_rate, frame_size, mel_bands)
    audio_analyzer.start()

def get_mel_bands():
    if audio_analyzer is not None:
        return audio_analyzer.get_mel_bands()
    return np.zeros(64, dtype=np.float32)

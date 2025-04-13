import numpy as np
import sounddevice as sd
import librosa

class AudioInput:
    def __init__(self, sample_rate=44100, frame_size=1024, channels=1, mel_bands=64):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.channels = channels
        self.mel_bands = mel_bands

        self.latest_samples = np.zeros(frame_size)
        self.volume = 0.0
        self.spectrum = np.zeros(frame_size // 2 + 1)
        self.mel_bands_data = np.zeros(mel_bands)

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            channels=self.channels,
            callback=self._audio_callback,
        )

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print("[Audio Warning]", status)

        samples = np.squeeze(indata)
        self.latest_samples = samples
        self.volume = np.linalg.norm(samples) / len(samples)

        # FFT
        self.spectrum = np.abs(np.fft.rfft(samples))

        # Mel Spectrogram
        mel = librosa.feature.melspectrogram(
            y=samples.astype(np.float32),
            sr=self.sample_rate,
            n_fft=self.frame_size,
            n_mels=self.mel_bands,
            fmax=self.sample_rate // 2
        )
        mel_db = librosa.power_to_db(mel, ref=np.max)
        mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-6)
        self.mel_bands_data = mel_norm[:, -1]  # Latest frame only

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def get_features(self):
        """Returns volume (float), spectrum (ndarray), mel_bands (ndarray)"""
        return self.volume, self.spectrum, self.mel_bands_data

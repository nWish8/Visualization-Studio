import numpy as np
import sounddevice as sd
import librosa
import threading
import queue

class AudioAnalyzer:
    def __init__(self, sample_rate=44100, frame_size=512, mel_bands=64):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.mel_bands = mel_bands
        self.audio_queue = queue.Queue(maxsize=10)
        self.latest_mel = np.zeros(self.mel_bands, dtype=np.float32)
        self.warning_count = 0

        # Start processing thread
        self.running = True
        self.processing_thread = threading.Thread(target=self.process_audio_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()

        # Start input stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            channels=1,
            callback=self.audio_callback,
            latency='low'
        )

    def audio_callback(self, indata, frames, time_info, status):
        if status:
            self.warning_count += 1
            if self.warning_count % 10 == 0:
                print(f"[Audio Warning] input overflow x{self.warning_count}")

        samples = indata[:, 0]  # mono
        try:
            self.audio_queue.put_nowait(samples.copy())
        except queue.Full:
            pass  # drop frame if overwhelmed

    def process_audio_loop(self):
        while self.running:
            try:
                samples = self.audio_queue.get(timeout=0.1)
                # ✅ Use n_fft no greater than sample length
                n_fft = min(len(samples), 512)

                mel = librosa.feature.melspectrogram(
                    y=samples.astype(np.float32),
                    sr=self.sample_rate,
                    n_fft=n_fft,
                    n_mels=self.mel_bands,
                    fmax=self.sample_rate / 2
                )
                mel_db = librosa.power_to_db(mel, ref=np.max)
                mel_norm = (mel_db - np.min(mel_db)) / (np.max(mel_db) - np.min(mel_db) + 1e-6)
                self.latest_mel = mel_norm[:, -1]
            except queue.Empty:
                continue

    def start(self):
        self.stream.start()

    def stop(self):
        self.running = False
        self.processing_thread.join()
        self.stream.stop()

    def get_mel_bands(self):
        return self.latest_mel.copy()

# Global instance
audio_analyzer = None

import sounddevice as sd

def find_best_input_device(prefer_loopback=True):
    devices = sd.query_devices()
    fallback = None

    for idx, dev in enumerate(devices):
        name = dev['name'].lower()
        if dev['max_input_channels'] > 0:
            if prefer_loopback and ('loopback' in name or 'stereo mix' in name):
                print(f"✅ Auto-selected loopback device: [{idx}] {dev['name']}")
                return idx, int(dev['default_samplerate'])
            elif fallback is None:
                fallback = (idx, int(dev['default_samplerate']))

    print(f"⚠️ No loopback found, using fallback device: [{fallback[0]}] {devices[fallback[0]]['name']}")
    return fallback

def initialize_audio(frame_size=512, mel_bands=64):
    global audio_analyzer
    input_device, sample_rate = find_best_input_device()
    sd.default.device = (input_device, None)

    audio_analyzer = AudioAnalyzer(
        sample_rate=sample_rate,
        frame_size=frame_size,
        mel_bands=mel_bands
    )
    audio_analyzer.start()

def get_mel_bands():
    if audio_analyzer is not None:
        return audio_analyzer.get_mel_bands()
    return np.zeros(64, dtype=np.float32)

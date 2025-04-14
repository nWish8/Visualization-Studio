import json
import moderngl_window as mglw
from visuals.grid_renderer import GridRenderer
from audio.audio_analysis import initialize_audio, get_mel_bands

class CymaticVisualizer(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Cymatic Visualizer"
    window_size = (1280, 720)
    resizable = True
    resource_dir = 'shaders'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load configuration from file
        with open("config/settings.json", "r") as f:
            self.settings = json.load(f)
        # Initialize live audio with configured settings
        initialize_audio(
            sample_rate=self.settings.get("sample_rate", 44100),
            frame_size=self.settings.get("frame_size", 1024),
            mel_bands=self.settings.get("mel_bands", 64)
        )
        # Create the grid renderer using the current OpenGL context and settings
        self.grid_renderer = GridRenderer(self.ctx, self.settings)

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.05, 0.05, 0.1)
        # Update grid audio texture using the latest Mel band data
        mel = get_mel_bands()
        self.grid_renderer.update_audio_texture(mel)
        self.grid_renderer.render(time)

    def resize(self, width: int, height: int):
        self.grid_renderer.resize(width, height)

if __name__ == '__main__':
    mglw.run_window_config(CymaticVisualizer)

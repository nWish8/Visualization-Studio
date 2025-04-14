import json
import moderngl_window as mglw
from visuals.grid_renderer import GridRenderer
from audio.audio_analysis import initialize_audio, get_mel_bands
import logging

# Set logging level
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# 🎧 Step 1: Load config and select audio device BEFORE window loads
with open("config/settings.json", "r") as f:
    settings = json.load(f)

initialize_audio()

class CymaticVisualizer(mglw.WindowConfig):
    title = "Cymatic Visualizer"
    window_size = (800, 800)
    resizable = True
    resource_dir = "."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.grid_renderer = GridRenderer(self.ctx, self.settings)

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.05, 0.05, 0.1)
        mel = get_mel_bands()
        self.grid_renderer.update_audio_texture(mel)
        self.grid_renderer.render(time)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

if __name__ == '__main__':
    mglw.run_window_config(CymaticVisualizer)

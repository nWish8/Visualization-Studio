import json
import moderngl_window as mglw
from visuals.grid_renderer import GridRenderer
from audio.audio_analysis import initialize_audio, get_mel_bands
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class CymaticVisualizer(mglw.WindowConfig):
    title = "Cymatic Visualizer"
    window_size = (800, 800)
    resizable = True
    resource_dir = "."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.debug("Loading configuration from config/settings.json")
        with open("config/settings.json", "r") as f:
            self.settings = json.load(f)
        
        logger.debug("Initializing audio analysis module")
        initialize_audio(
            sample_rate=self.settings.get("sample_rate", 44100),
            frame_size=self.settings.get("frame_size", 1024),
            mel_bands=self.settings.get("mel_bands", 64)
        )
        
        logger.debug("Creating GridRenderer object")
        self.grid_renderer = GridRenderer(self.ctx, self.settings)

    # Implement the required on_render method.
    def on_render(self, time: float, frame_time: float):
        # Clear the screen to a dark blue color.
        self.ctx.clear(0.05, 0.05, 0.1)
        # Update the audio texture with the latest mel band data.
        mel = get_mel_bands()
        self.grid_renderer.update_audio_texture(mel)
        # Delegate rendering to GridRenderer.
        self.grid_renderer.render(time)

    # Optionally, you may keep a render() method to separate logic (and call it from on_render)
    def render(self, time: float, frame_time: float):
        # This method is not automatically called if on_render is not implemented.
        # You can use this for additional logic if you prefer.
        self.on_render(time, frame_time)

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

if __name__ == '__main__':
    mglw.run_window_config(CymaticVisualizer)

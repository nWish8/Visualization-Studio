import json
import logging
import numpy as np
import moderngl_window as mglw

from visuals.grid_renderer import GridRenderer
from audio.audio_analysis import (
    initialize_audio,
    get_mel_bands,
)

# Logging setup
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Load settings
def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

settings = load_settings()
initialize_audio()

def perspective(fovy, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fovy) / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype='f4')

def look_at(eye, target, up=(0, 1, 0)):
    eye, target, up = map(np.array, (eye, target, up))
    f = target - eye
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    u = np.cross(s, f)

    m = np.identity(4, dtype=np.float32)
    m[0, :3] = s
    m[1, :3] = u
    m[2, :3] = -f
    m[:3, 3] = -np.dot(m[:3, :3], eye)
    return m

class CymaticVisualizer(mglw.WindowConfig):
    title = "Cymatic Visualizer"
    window_size = (800, 800)
    resizable = True
    resource_dir = "."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.grid_renderer = GridRenderer(self.ctx, self.settings)
        self.eye = self.settings["camera"]["position"]
        self.target = self.settings["camera"]["look_at"]
        self.fov = 60.0

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.05, 0.05, 0.1)
        mel = get_mel_bands()
        proj = perspective(self.fov, self.wnd.aspect_ratio, 0.1, 100.0)
        view = look_at(self.eye, self.target)
        self.grid_renderer.update_spectrum(mel)
        self.grid_renderer.render(proj, view, time)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS and key == self.wnd.keys.R:
            print("🔁 Reloading settings.json...")
            new_settings = load_settings()
            self.settings.update(new_settings)
            self.grid_renderer.settings = self.settings

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

if __name__ == '__main__':
    mglw.run_window_config(CymaticVisualizer)
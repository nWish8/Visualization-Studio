import json
import logging
import numpy as np
import moderngl_window as mglw

from visuals.grid_renderer import GridRenderer
from audio.audio_analysis import (
    initialize_audio,
    get_mel_bands,
    device_names,
    current_device_index,
    switch_audio_device,
)

# Logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Load configuration
def load_settings():
    with open("config/settings.json", "r") as f:
        return json.load(f)

settings = load_settings()
initialize_audio()

# Basic perspective projection matrix
def perspective(fovy, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fovy) / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype='f4')

# Basic look-at camera matrix
def look_at(eye, target, up=(0, 1, 0)):
    eye = np.array(eye, dtype=np.float32)
    target = np.array(target, dtype=np.float32)
    up = np.array(up, dtype=np.float32)

    f = (target - eye)
    f /= np.linalg.norm(f)
    u = up / np.linalg.norm(up)
    s = np.cross(f, u)
    u = np.cross(s, f)

    m = np.identity(4, dtype=np.float32)
    m[0, :3] = s
    m[1, :3] = u
    m[2, :3] = -f
    m[0, 3] = -np.dot(s, eye)
    m[1, 3] = -np.dot(u, eye)
    m[2, 3] = np.dot(f, eye)
    return m

class CymaticVisualizer(mglw.WindowConfig):
    title = "Cymatic Visualizer"
    window_size = (800, 800)
    resizable = True
    resource_dir = "."
    aspect_ratio = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.grid_renderer = GridRenderer(self.ctx, self.settings)

        # 🎥 Camera setup from config
        self.eye = np.array(self.settings["camera"]["position"])
        self.target = np.array(self.settings["camera"]["look_at"])
        self.fov = 60.0

    def on_render(self, time: float, frame_time: float):
        self.ctx.clear(0.05, 0.05, 0.1)
        mel = get_mel_bands()

        aspect = self.wnd.aspect_ratio
        projection = perspective(self.fov, aspect, 0.1, 100.0)
        view = look_at(self.eye, self.target)

        self.grid_renderer.update_spectrum(mel)
        self.grid_renderer.render(projection, view, time)

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.R:
                print("🔁 Reloading settings.json...")
                new_settings = load_settings()
                self.settings.update(new_settings)
                self.grid_renderer.settings = self.settings

            elif key == self.wnd.keys.UP:
                self.settings["grid"]["height_scale"] += 0.1
                print(f"⬆️  Height scale: {self.settings['grid']['height_scale']:.2f}")
            elif key == self.wnd.keys.DOWN:
                self.settings["grid"]["height_scale"] = max(0.0, self.settings["grid"]["height_scale"] - 0.1)
                print(f"⬇️  Height scale: {self.settings['grid']['height_scale']:.2f}")
            elif key == self.wnd.keys.RIGHT:
                self.settings["visuals"]["point_size"] += 0.2
                print(f"➡️  Point size: {self.settings['visuals']['point_size']:.2f}")
            elif key == self.wnd.keys.LEFT:
                self.settings["visuals"]["point_size"] = max(1.0, self.settings["visuals"]["point_size"] - 0.2)
                print(f"⬅️  Point size: {self.settings['visuals']['point_size']:.2f}")

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

if __name__ == '__main__':
    mglw.run_window_config(CymaticVisualizer)

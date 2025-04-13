import numpy as np
import moderngl
import moderngl_window as mglw
from audio_input import get_mel_bands


class CymaticVisualizer(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Cymatic Visualizer"
    window_size = (1280, 720)
    aspect_ratio = None
    resizable = True
    resource_dir = 'shaders'  # still useful for textures, fonts, etc.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Grid resolution
        self.grid_res = 128
        self.grid_size = self.grid_res * self.grid_res

        # Vertex buffer: grid of x,z points from -1 to 1
        x = np.linspace(-1, 1, self.grid_res)
        z = np.linspace(-1, 1, self.grid_res)
        grid = np.array([(i, 0.0, j) for j in z for i in x], dtype='f4')
        self.vbo = self.ctx.buffer(grid.tobytes())

        # Index buffer for drawing triangles
        indices = []
        for row in range(self.grid_res - 1):
            for col in range(self.grid_res - 1):
                i = row * self.grid_res + col
                indices += [i, i + 1, i + self.grid_res,
                            i + 1, i + self.grid_res + 1, i + self.grid_res]
        self.ibo = self.ctx.buffer(np.array(indices, dtype='i4').tobytes())

        # Load shaders directly
        with open("shaders/grid.vert") as f:
            vertex_shader = f.read()
        with open("shaders/grid.frag") as f:
            fragment_shader = f.read()

        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader,
        )

        self.program['resolution'].value = self.grid_res

        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_position')],
            self.ibo
        )

        # Audio texture (1D)
        self.audio_data = np.zeros(self.grid_res, dtype='f4')
        self.audio_texture = self.ctx.texture((self.grid_res,1), 1, self.audio_data.tobytes())
        self.audio_texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.program['audio_texture'] = 0

        self.time = 0.0

    def render(self, time: float, frame_time: float):
        self.ctx.clear(0.0, 0.0, 0.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        self.time = time
        self.program['time'].value = self.time

        # Update mel band data
        self.audio_data = get_mel_bands(self.grid_res)
        self.audio_texture.write(self.audio_data.tobytes())
        self.audio_texture.use(location=0)

        # Draw grid
        self.vao.render()

    def resize(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)


if __name__ == '__main__':
    mglw.run_window_config(CymaticVisualizer)

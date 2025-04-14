import moderngl
import numpy as np
from pathlib import Path

class GridRenderer:
    def __init__(self, ctx: moderngl.Context, settings):
        self.ctx = ctx
        self.settings = settings
        self.grid_res = settings.get("grid_resolution", 128)
        self._create_program()
        self._create_geometry()
        self._create_audio_texture()

    def _create_program(self):
        vertex_path = Path("shaders/vertex_shader.glsl")
        fragment_path = Path("shaders/fragment_shader.glsl")
        self.vertex_shader_source = vertex_path.read_text()
        self.fragment_shader_source = fragment_path.read_text()

        self.program = self.ctx.program(
            vertex_shader=self.vertex_shader_source,
            fragment_shader=self.fragment_shader_source,
        )

        if "time" in self.program:
            self.program["time"].value = 0.0
        if "audio_texture" in self.program:
            self.program["audio_texture"].value = 0

    def _create_geometry(self):
        vertices = []
        indices = []
        res = self.grid_res

        for row in range(res):
            for col in range(res):
                x = (col / (res - 1)) * 2.0 - 1.0
                z = (row / (res - 1)) * 2.0 - 1.0
                vertices.extend([x, 0.0, z])

        vertices = np.array(vertices, dtype='f4')
        self.vbo = self.ctx.buffer(vertices.tobytes())

        for row in range(res - 1):
            for col in range(res - 1):
                i = row * res + col
                indices.extend([
                    i, i + 1, i + res,
                    i + 1, i + res + 1, i + res
                ])

        indices = np.array(indices, dtype='i4')
        self.ibo = self.ctx.buffer(indices.tobytes())
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "3f", "in_position")], self.ibo)

    def _create_audio_texture(self):
        self.audio_data = np.zeros(self.grid_res, dtype='f4')
        self.audio_texture = self.ctx.texture((self.grid_res, 1), 1, self.audio_data.tobytes(), dtype='f4')
        self.audio_texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        if "audio_texture" in self.program:
            self.program["audio_texture"].value = 0

    def update_audio_texture(self, mel_data: np.ndarray):
        if mel_data.shape[0] != self.grid_res:
            mel_data = np.resize(mel_data, (self.grid_res,))
        self.audio_data = mel_data.astype('f4')
        self.audio_texture.write(self.audio_data.tobytes())

    def render(self, time: float):
        if "time" in self.program:
            self.program["time"].value = time
        self.audio_texture.use(location=0)
        self.vao.render(moderngl.TRIANGLES)
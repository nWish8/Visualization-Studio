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

        # Debug: List active uniforms.
        # print("Active uniforms in shader:")
        # for name in self.program:
        #     print("  ", name)

        def set_uniform_safe(name, value):
            if name in self.program:
                self.program[name].value = value
            else:
                print(f"[Warning] Uniform '{name}' not found in shader.")
                
        # Set uniform "resolution" as a vec2.
        set_uniform_safe("resolution", (float(self.grid_res), float(self.grid_res)))
        # Set "color" from settings.
        color = self.settings.get("color", {"r": 0.2, "g": 0.7, "b": 1.0, "a": 1.0})
        set_uniform_safe("color", (color["r"], color["g"], color["b"], color["a"]))
        # Set initial "time" uniform.
        if "time" in self.program:
            self.program["time"].value = 0.0
        # Set "audio_texture" uniform to texture unit 0.
        if "audio_texture" in self.program:
            self.program["audio_texture"].value = 0
        else:
            print("[Warning] Uniform 'audio_texture' not found in shader.")

    def _create_geometry(self):
        # Generate grid vertices on the XZ plane in the range [-1, 1].
        vertices = []
        for row in range(self.grid_res):
            for col in range(self.grid_res):
                x = (col / (self.grid_res - 1)) * 2.0 - 1.0
                z = (row / (self.grid_res - 1)) * 2.0 - 1.0
                vertices.extend([x, 0.0, z])
        self.vertex_data = np.array(vertices, dtype='f4')
        self.vbo = self.ctx.buffer(self.vertex_data.tobytes())
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, "in_position")

    def _create_audio_texture(self):
        # Create a 1D texture with size (grid_res, 1) to hold the mel band data.
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
        self.vao.render(moderngl.POINTS)

import numpy as np
import moderngl
from pathlib import Path

class GridRenderer:
    def __init__(self, ctx, settings):
        self.ctx = ctx
        self.grid_res = settings.get("grid_resolution", 128)
        self.height_scale = settings.get("height_scale", 1.0)
        self._create_program()
        self._create_geometry()
        self._create_spectrum_texture()

    def _create_program(self):
        self.program = self.ctx.program(
            vertex_shader=Path("shaders/grid_shader.glsl").read_text(),
            varyings=["out_color"],  # if using transform feedback (optional)
        )


    def _create_geometry(self):
        # Generate a flat grid of points on the XZ plane
        res = self.grid_res
        vertices = []
        for z in range(res):
            for x in range(res):
                xpos = (x / (res - 1)) * 2 - 1  # Normalized X [-1, 1]
                zpos = (z / (res - 1)) * 2 - 1  # Normalized Z [-1, 1]
                vertices.extend([xpos, 0.0, zpos])  # Y=0, will be displaced

        # Convert to numpy float32 and upload to GPU
        self.vertex_data = np.array(vertices, dtype='f4')
        self.vbo = self.ctx.buffer(self.vertex_data.tobytes())

        # Bind vertex buffer to VAO with 3f per vertex (vec3)
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, "3f", "in_position")])

    def _create_spectrum_texture(self):
        # Create 1024-point audio spectrum texture (1D)
        self.spectrum_data = np.zeros(1024, dtype='f4')
        self.spectrum_tex = self.ctx.texture((1024, 1), 1, self.spectrum_data.tobytes(), dtype='f4')
        self.spectrum_tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.program['spectrum'] = 0  # Bind to texture unit 0

    def update_spectrum(self, spectrum):
        # Normalize and upload new spectrum data each frame
        spectrum = np.resize(spectrum, 1024).astype('f4')
        self.spectrum_tex.write(spectrum.tobytes())

    def render(self, projection, view, time):
        # Pass matrices and time to shader
        self.program['projection'].write(projection.astype('f4').tobytes())
        self.program['view'].write(view.astype('f4').tobytes())
        self.program['time'].value = time

        # Bind spectrum texture and draw grid
        self.spectrum_tex.use(location=0)
        self.vao.render(moderngl.POINTS)
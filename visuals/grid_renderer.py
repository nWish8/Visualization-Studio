import moderngl
import moderngl_window as mglw
from pathlib import Path

class GridRenderer:
    def __init__(self, ctx: moderngl.Context, settings):
        self.ctx = ctx
        self.settings = settings
        self.grid_res = settings.get("grid_resolution", 10)
        self._create_program()

    def _create_program(self):
        vertex_path = Path("shaders/vertex_shader.glsl")
        fragment_path = Path("shaders/fragment_shader.glsl")

        self.program = self.ctx.program(
            vertex_shader=vertex_path.read_text(),
            fragment_shader=fragment_path.read_text(),
        )

        print("Active uniforms in shader:")
        for name in self.program:
            print("  ", name)

        # Safe uniform setting
        def set_uniform_safe(name, value):
            if name in self.program:
                self.program[name].value = value
            else:
                print(f"[Warning] Uniform '{name}' not found in shader.")

        # Setting known uniforms
        set_uniform_safe("resolution", (self.grid_res, self.grid_res))
        set_uniform_safe("color", (1.0, 0.3, 0.5, 1.0))

    def render(self, time):
        if "time" in self.program:
            self.program["time"].value = time

        # render logic goes here (VBO draw, etc.)

#version 330

in vec3 in_position;

uniform float time;
uniform sampler1D audio_texture;
uniform int resolution;

void main() {
    int x = gl_VertexID % resolution;
    int z = gl_VertexID / resolution;
    float u = float(x) / float(resolution - 1);

    float audio_val = texture(audio_texture, u).r;

    vec3 pos = in_position;
    pos.y += audio_val * 0.5;

    gl_Position = vec4(pos, 1.0);
}

#version 330

uniform float time;
uniform sampler1D audio_texture;

in vec3 in_position;
out float vHeight;
out vec3 vColor;

void main() {
    float u = (in_position.x + 1.0) / 2.0;
    float v = (in_position.z + 1.0) / 2.0;

    float audio_val = texture(audio_texture, u).r;

    float wave = sin((in_position.x + time) * 4.0) * 0.1;
    float ripple = sin((in_position.z - time * 0.3) * 8.0) * 0.1;

    vec3 pos = in_position;
    pos.y += audio_val * 0.4 + wave + ripple;

    gl_Position = vec4(pos, 1.0);

    vHeight = pos.y;
    vColor = vec3(audio_val, v, 1.0 - u);
}
#version 330

uniform mat4 projection;
uniform mat4 view;
uniform float time;
uniform sampler1D spectrum;

in vec3 in_position;
out vec4 out_color;

void main() {
    vec3 pos = in_position;

    // Example use of `time` — modulate wave animation
    float s = texture(spectrum, pos.x * 0.5 + 0.5).r;
    pos.z += sin(time + pos.x * 4.0) * 0.1 + s * 0.5;

    gl_Position = projection * view * vec4(pos, 1.0);
    out_color = vec4(vec3(s), 1.0);
}

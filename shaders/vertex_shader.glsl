#version 330

// Uniform declarations (must match exactly between vertex and fragment shaders)
uniform vec2 resolution;         // Added: resolution is now a vec2 in both shaders.
uniform sampler1D audio_texture;
uniform float time;

in vec3 in_position;

void main() {
    // Convert the x coordinate from [-1,1] to [0,1] for texture sampling.
    float u = (in_position.x + 1.0) / 2.0;
    float audio_val = texture(audio_texture, u).r;

    vec3 pos = in_position;
    // Displace vertex in Y by combining audio value and a time–based sine modulation.
    pos.y += audio_val * 0.5 * sin(time * 2.0 + in_position.z * 3.1415);

    gl_Position = vec4(pos, 1.0);
}

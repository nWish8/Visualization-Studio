#version 330

uniform mat4 projection;             // Projection matrix (perspective)
uniform mat4 view;                   // View matrix (camera)
uniform float time;                  // Time for animations (not currently used)
uniform float height_scale;          // Controls how high the terrain displaces
uniform sampler1D spectrum;          // 1D texture containing audio spectrum data

in vec3 in_position;                 // Incoming vertex position
out vec3 vColor;                     // Output color to fragment shader

void main() {
    // Compute radial distance from origin (used to sample spectrum texture)
    float u = length(in_position.xz);

    // Sample audio intensity from spectrum texture using distance as UV
    float audio = texture(spectrum, clamp(u, 0.0, 1.0)).r;

    // Displace vertex along Y based on spectrum value and height scale
    vec3 pos = in_position;
    pos.y += audio * height_scale;

    // Transform vertex position to clip space
    gl_Position = projection * view * vec4(pos, 1.0);

    // Set vertex color based on audio intensity
    vColor = vec3(audio * 0.8, 0.5 * audio, 1.0 - audio);
}
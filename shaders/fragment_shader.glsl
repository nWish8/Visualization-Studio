#version 330

uniform vec2 resolution;  // Declared as vec2 (must match the vertex shader)
uniform float time;
uniform vec4 color;

out vec4 fragColor;

void main() {
    // Calculate UV coordinates from fragment coordinates.
    vec2 uv = gl_FragCoord.xy / resolution;
    // Create a simple pulsing effect.
    float intensity = 0.5 + 0.5 * sin(time + uv.x * 10.0);
    fragColor = vec4(color.rgb * intensity, color.a);
}

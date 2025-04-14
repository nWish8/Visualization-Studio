#version 330

uniform vec2 resolution;
uniform float time;
uniform vec4 color;

out vec4 fragColor;

void main() {
    // Normalize pixel coordinates
    vec2 uv = gl_FragCoord.xy / resolution.xy;

    // A simple pulsing effect for now
    float intensity = 0.5 + 0.5 * sin(time + uv.x * 10.0);
    fragColor = vec4(color.rgb * intensity, color.a);
}

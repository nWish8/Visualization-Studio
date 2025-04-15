#version 330

uniform float time;


in vec3 vColor;          // Interpolated color from vertex shader
out vec4 fragColor;      // Final pixel color

void main() {
    fragColor = vec4(vColor, 1.0);  // Opaque fragment output
}
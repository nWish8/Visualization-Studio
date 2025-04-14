#version 330

in float vHeight;
in vec3 vColor;
out vec4 fragColor;

void main() {
    float brightness = smoothstep(-0.1, 0.5, vHeight);
    fragColor = vec4(vColor * brightness, 1.0);
}
# En openGl los shadders se escriben en lenguaje GLSL (OpenGL Shading Language)

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec4 outColor;
out vec2 UVs;

void main(){
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;
}
'''


fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; 

in vec2 UVs;

out vec4 fragColor;

void main(){
    fragColor = texture(tex, UVs);
}
'''
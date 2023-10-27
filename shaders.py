# En openGl los shadders se escriben en lenguaje GLSL (OpenGL Shading Language)

vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 inColor;

out vec4 outColor;

void main(){
    gl_Position = vec4(position, 1.0f);
    outColor = vec4(inColor, 1.0f);
}
'''


fragment_shader = '''
#version 450 core

in vec4 outColor;
out vec4 fragColor;

void main(){
    fragColor = outColor;
}

'''
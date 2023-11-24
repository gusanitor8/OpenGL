# En openGl los shadders se escriben en lenguaje GLSL (OpenGL Shading Language)

wobbly_vertex_shader = '''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform float time;

out vec2 UVs;
out vec3 outNormals;


void main(){
    vec3 pos = position;
    pos.y = pos.y + sin(time + pos .x);
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(pos, 1.0);
    UVs = texCoords;
    outNormals = (modelMatrix * vec4(normals, 0.0)).xyz;
    outNormals = normalize(outNormals);
}
'''

vertex_shader = """
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoords;
layout (location = 2) in vec3 normals;
layout (location = 3) in float time;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 outNormals;

void main(){
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    UVs = texCoords;
    outNormals = normalize((modelMatrix * vec4(normals, 0.0)).xyz);
}
"""


fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; 

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;
uniform float time;

out vec4 fragColor;

void main(){
    float intensity = dot(outNormals, -dirLight);
    intensity = min(1, intensity);
    intensity = max(0, intensity);        
    fragColor = texture(tex, UVs);
    
    fragColor.x = mod((fragColor.x + sin(time)), 1.0);
}
'''

acid_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; 

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;
uniform float time;
uniform vec3 camPos;

out vec4 fragColor;

void main(){
    float intensity = dot(outNormals, -dirLight);
    intensity = min(1, intensity);
    intensity = max(0, intensity);        
    fragColor = texture(tex, UVs);

    fragColor.x = mod((fragColor.y + sin(time)), 1.0);
    fragColor.y = mod((fragColor.x + sin(time)), 1.0);
}
'''

gloomy_fragment_shader = '''
#version 450 core

layout (binding = 0) uniform sampler2D tex; 

uniform vec3 dirLight;
uniform float time;
uniform vec3 camPos;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main(){
    float intensity = dot(outNormals, -dirLight);
    
    // float gloom = dot(outNormals, -camPos);
    // vec3 yellow = vec3(0,1,1) * gloom;
    // intensity += yellow;
    
    intensity = min(1, intensity);
    intensity = max(0, intensity);  
            
    fragColor = texture(tex, UVs) * intensity;

}
'''

#shader vertex
#version 330 core

layout(location = 0) in vec3 vPos;

out vec3 fPos;

uniform mat4 uTransform;
uniform mat4 uProj;

void main() {
	fPos = vec3(uTransform * vec4(vPos,1));
	gl_Position = uProj * vec4(fPos,1);
}

#shader fragment
#version 330 core

layout(location = 0) out vec4 oColor;

in vec3 fPos;

void main() {
	oColor = vec4(1,1,1, 1);
}
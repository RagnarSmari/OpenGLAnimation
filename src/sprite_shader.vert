#version 330 core
attribute vec3 a_position;
attribute vec2 a_uv; // uv

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

varying vec2 v_uv; // uv 


void main(void)
{
    vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    
	//UV COORDS sent into per-pixel use
	v_uv = a_uv;

    // Local Coordinates
    position = u_model_matrix * position;

    // Global coordinates

    position = u_view_matrix * position;
    // Eye Coordinates
    
    position = u_projection_matrix * position;
    // Clip Coordinates

    gl_Position = position;
}
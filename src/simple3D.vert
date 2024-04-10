#version 330 core
attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv; // uv



uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

// uniform vec4 u_color;
uniform vec4 u_eye_position;

uniform vec4 u_light_position;


varying vec4 v_color;  //Leave the varying variables alone to begin with

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv; // uv 


void main(void)
{
    vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
    
	//UV COORDS sent into per-pixel use
	v_uv = a_uv;

    // Local Coordinates
    position = u_model_matrix * position;
    v_normal = normalize(u_model_matrix * normal);

    // Gloabal Coordinates
    v_s = normalize(u_light_position - position);

    vec4 h = normalize(u_eye_position - position);
    v_h = normalize(v_s + h);

    // float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
    // float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
    // v_color = (light_factor_1 + light_factor_2) * u_color; 



    position = u_view_matrix * position;
    // Eye Coordinates
    
    position = u_projection_matrix * position;
    // Clip Coordinates

    gl_Position = position;
}
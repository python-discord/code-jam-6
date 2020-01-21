---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3  v_pos;
attribute vec3  v_normal;
attribute vec2  v_tc0;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;

varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec2 tex_coord0;
varying int id;

void main (void) {
    vec4 pos = modelview_mat * vec4(v_pos, 1.0);
    vertex_pos = pos;
    normal_vec = vec4(v_normal, 0.0);
    gl_Position = projection_mat * pos;

    tex_coord0 = v_tc0;
    id = gl_VertexID;}

---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 normal_vec;
varying vec4 vertex_pos;

uniform mat4 normal_mat;
uniform vec3 id_color;

varying vec2 tex_coord0;
varying int id;

void main (void){
    id = id_color.x;
    gl_FragColor.x = id;
    gl_FragColor.y = tex_coord0.x;
    gl_FragColor.z = tex_coord0.y;
    gl_FragColor.a = 1.0;}

// Same as simple.glsl except we save vertex texture coordinates into a 256x256 texture
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


void main (void) {
    vec4 pos = modelview_mat * vec4(v_pos, 1.0);
    vertex_pos = pos;
    normal_vec = vec4(v_normal,0.0);
    tex_coord0 = v_tc0;
    gl_Position = projection_mat * camera * pos;
}

---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 normal_vec;
varying vec4 vertex_pos;

uniform mat4 normal_mat;
uniform vec3 id_color;

varying vec2 tex_coord0;
float id;

void main (void){
    id = id_color.x;
    gl_FragColor.x = id;
    gl_FragColor.y = tex_coord0.x;
    gl_FragColor.z = tex_coord0.y;
    gl_FragColor.a = 1.0;}

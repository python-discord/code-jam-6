'''
Modified 3D Rotating Monkey Head example -- rotation can be controlled with mouse.
'''
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from objloader import ObjFile

ROTATE_SPEED = 500


class Renderer(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = 'simple.glsl'
        self.scene = ObjFile('monkey.obj') # We'll want to generate meshes on-the-fly instead.
                                           # I assume a triangulated random cloud of points
                                           # will be stony enough. We should be able to remove
                                           # all dependency on objloader though. Then again, if
                                           # we add save/load methods we may want objloader.
        self.collision_fbo = Fbo(size=(256, 256),       # Last attempt at collision detection
                                 with_depthbuffer=True, # using a fbo to save rendered vertices.
                                 compute_normal_mat=True,
                                 clear_color = (0.0,) * 4)
        self.collision_fbo.shader.source = 'collision.glsl'
        self.setup_scene()
        self.indices = self.mesh.indices.copy()
        self.fewer = self.indices[3:]

        def set_aspect():
            asp = self.width / self.height
            proj = Matrix().view_clip(-asp, asp, -1, 1, .5, 100, 1)
            self.canvas['projection_mat'] = self.collision_fbo['projection_mat'] = proj
        Clock.schedule_once(lambda dt: set_aspect())

    def on_touch_move(self, touch):
        """
        We should have two different drags --- one to rotate the stone and one to chip the
        stone.  Probably 'right' and 'left' click differentiated.
        """
        if touch.button == 'right':
            self.rotate(touch.dsx)
        else:
            self.chip_away(touch)

    def chip_away(self, touch):
        """
        Need collision detection with mesh and a method to remove points from mesh.  I think
        this function will be the most difficult to flesh out.
        """

        if self.mesh.indices == self.indices:
            print(touch.spos)
            pixels = self.collision_fbo.pixels
            touch_index = 4 * int(touch.sy * 256**2 + touch.sx * 256)
            print(touch_index)
            print(pixels[touch_index:touch_index + 4])

        #self.mesh.indices = self.mesh.indices[3:] # This makes a pretty creepy monkey.

    def rotate(self, dx):
        self.rotx.angle += dx * ROTATE_SPEED

    def setup_scene(self):
        with self.canvas:
            self.cb = Callback(lambda *args: glEnable(GL_DEPTH_TEST))
            self.translate = Translate(0, 0, -2) # Maybe zoom in more?
            self.rotx = Rotate(0, 0, 1, 0)
            m, *_ = self.scene.objects.values()
            UpdateNormalMatrix()
            self.mesh = Mesh(vertices=m.vertices,
                             indices=m.indices,
                             fmt=m.vertex_format,
                             mode='triangles')
            self.cb = Callback(lambda *args: glDisable(GL_DEPTH_TEST))
        with self.collision_fbo:
            self.cb = Callback(lambda *args: glEnable(GL_DEPTH_TEST))
            self.translate
            self.rotx
            UpdateNormalMatrix()
            self.mesh
            self.cb = Callback(lambda *args: glDisable(GL_DEPTH_TEST))

class RendererApp(App):
    def build(self):
        return Renderer()

if __name__ == "__main__":
    RendererApp().run()
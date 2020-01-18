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
from kivy.core.window import Window
from math import cos, sin, pi

def to_radians(x):
    return x / 360 * 2 * pi

class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = 'simple.glsl'
        self.scene = ObjFile('monkey.obj') # We'll want to generate meshes on-the-fly instead.
                                           # I assume a triangulated random cloud of points
                                           # will be stony enough. We should be able to remove
                                           # all dependency on objloader though. Then again, if
                                           # we add save/load methods we may want objloader --
                                           # could use a bit of rewrite in that case.
        super().__init__(**kwargs)

        with self.canvas:
            self.cb = Callback(lambda *args: glEnable(GL_DEPTH_TEST))
            self.setup_scene()
            self.cb = Callback(lambda *args: glDisable(GL_DEPTH_TEST))

        Window.bind(on_touch_move=self._on_touch_move)

        def set_aspect():
            asp = self.width / self.height
            proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
            self.canvas['projection_mat'] = proj
        Clock.schedule_once(lambda dt: set_aspect())

    def _on_touch_move(self, instance, touch):
        """
        We should have two different drags --- one to rotate the stone and one to chip the
        stone.  Probably 'right' and 'left' click differentiated.
        """
        if touch.button == 'right':
            self.rotate(touch.dsx, -touch.dsy)
        else:
            self.chip_away(touch)

    def chip_away(self, touch):
        """
        Need collision detection with mesh and a method to remove points from mesh.  Just
        popping vertices/indices from the mesh doesn't seem to change the object on the canvas.
        I think this function will be the most difficult to flesh out.

        Ok, to update the mesh indices, the list needs to be changed. That's why popping didn't
        work.
        """
        self.mesh.indices = self.mesh.indices[8:]

    def rotate(self, dx, dy):
        x = to_radians(self.rotx.angle)
        self.rotx.angle += dx * 500 # Hard-coded 500 should be a constant
        self.roty.angle += dy * 500 * cos(x) # Rotation is still a bit off -- probably need
        self.rotz.angle += dy * 500 * sin(x) # to account for more than just rotx.angle.


    def setup_scene(self):
        Translate(0, 0, -2) # Maybe zoom in more?
        self.rotx = Rotate(0, 0, 1, 0)
        self.roty = Rotate(0, 1, 0, 0)
        self.rotz = Rotate(0, 0, 0, 1)
        m, *_ = self.scene.objects.values()
        UpdateNormalMatrix()
        self.mesh = Mesh(vertices=m.vertices,
                         indices=m.indices,
                         fmt=m.vertex_format,
                         mode='triangles')

class RendererApp(App):
    def build(self):
        return Renderer()

if __name__ == "__main__":
    RendererApp().run()
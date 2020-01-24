from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Point
from kivy.uix.widget import Widget

from .abacus import Abacus

class AbacusControl(FloatLayout):

    def __init__(self, ** kwargs):
        super(AbacusControl, self).__init__(** kwargs)
        
    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        beads = Abacus().getBeads()
        for col in beads:
            for b in col:
                for x in (b.down):
                    print(x.pos[0],x.pos[1], x.pos[0] + x.size[0]*-1, x.pos[1] + x.size[1]*-1)
        print(touch.pos)
        '''
        if(touch.pos[0] > x.pos[0]
           and touch.pos[0] < x.pos[0] + x.size[0]*-1
           and touch.pos[1] > x.pos[1]
           and touch.pos[1] < x.pos[1] + x.size[1]*-1):
            print('found')
        '''
    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        '''
        if(self.in_pad and touch.pos[0] > self.pos[0]
           and touch.pos[0] < self.pos[0] + self.size[0]
           and touch.pos[1] > self.pos[1]
           and touch.pos[1] < self.pos[1] + self.size[1]):
            self.ud = touch.ud

            points = self.ud['lines'][-1].points
            oldx, oldy = points[-2], points[-1]
            points = calculate_points(oldx, oldy, touch.x, touch.y)
            if points:
                try:
                    lp = self.ud['lines'][-1].add_point
                    for idx in range(0, len(points), 2):
                        lp(points[idx], points[idx + 1])
                except GraphicException:
                    pass
        '''

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        '''
        self.ud = touch.ud
        if self.in_pad:
            self.in_pad = False
        '''
    '''
    def getBeads(self):
        return (self.top_beads, self.bottom_beads)
    
    def animationTest(self):
        def test():
          t1 = Thread(target=self.preset(123456789))
          t1.start()
          t1.join()
          sleep(1)
          t2 = Thread(target=self.reset())
          t2.start()

        Thread(target=test).start()
    '''



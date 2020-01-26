from collections import deque

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout

from math import floor

from threading import Thread

from time import sleep


class Bead(Rectangle):
    def __init__(self, **kwargs):
        super(Bead, self).__init__(source='assets/graphics/bead.png', **kwargs)

        self.anim = None

    def get_anim_offset(self):
        if not self.anim:
            return 0

        return 1 - (self.anim.progress - 1) ** 2


class AbacusColumn(FloatLayout):
    def __init__(self, n_beads, parent, **kwargs):
        super(AbacusColumn, self).__init__(**kwargs)

        self.abacus = parent
    
        self.n_beads = n_beads
        self.up = []
        self.down = []

        for i in range(n_beads):
            self.down.append(Bead())

    def on_touch_down(self, touch):
        for bead in self.up + self.down:
            if bead.anim is not None:
                return

        self.abacus.update()

        tx, ty = touch.pos
        x, y = self.pos
        w, h = self.size

        if x < tx and x + w > tx and y < ty and y + h > ty:            
            for i in range(len(self.down)):
                x, y = self.down[i].pos
                w, h = self.down[i].size

                if x < tx and x + w > tx and y < ty and y + h > ty:
                    anim = AbacusAnim()
                    anim.add_shift_up(self, i + 1)

                    Thread(target=self.abacus.build_anim(anim)).start()

                    return

            for i in range(len(self.up)):
                x, y = self.up[i].pos
                w, h = self.up[i].size

                if x < tx and x + w > tx and y < ty and y + h > ty:
                    anim = AbacusAnim()
                    anim.add_shift_down(self, i + 1)

                    Thread(target=self.abacus.build_anim(anim)).start()

                    return

    def shift_up(self, n):
        if n == -1:
            n = len(self.down)

        if len(self.down) < n:
            return False

        for i in range(n):
            self.up.append(self.down.pop())

    def shift_down(self, n):
        if n == -1:
            n = len(self.up)

        if len(self.up) < n:
            return False

        for i in range(n):
            self.down.append(self.up.pop())

        return len(self.up)


class AbacusAnim:
    ANIM_SPEED = 50

    def __init__(self):
        self.progress = 0
        self.speed = self.ANIM_SPEED

        self.up_shifts = []
        self.down_shifts = []

    def add_shift_up(self, column, n_beads):
        if n_beads == -1:
            n_beads = len(column.down)

        self.up_shifts.append((column, n_beads))

    def add_shift_down(self, column, n_beads):
        if n_beads == -1:
            n_beads = len(column.up)

        self.down_shifts.append((column, n_beads))


class Abacus(FloatLayout):
    MAX_BAR_W = 10
    MIN_BORDER_W = 16
    MIN_BEAD_SPACING = 4

    N_BARS = 12
    N_TOP_BEADS = 1
    N_BOTTOM_BEADS = 4

    TOP_V = N_BOTTOM_BEADS + 1
    PLACE = (N_TOP_BEADS + 1) * TOP_V

    ANIM_CLOCK_CYCLE = 0.003

    def __init__(self, **kwargs):
        super(Abacus, self).__init__(**kwargs)

        self.bar_w = self.MAX_BAR_W

        with self.canvas:
            Color(1, 1, 1, 1)

            self.border = []

            for i in range(4):
                self.border.append(Rectangle(source=App.get_running_app().TEXTURE))

            Color(1, 1, 1, 0.2)

            self.border_highlight = [Rectangle(), Rectangle()]

            Color(1, 1, 1, 1)

            self.divider = Rectangle(source=App.get_running_app().TEXTURE)

            Color(1, 1, 1, 0.2)

            self.border_highlight.append(Rectangle())

            self.bar_rects = []
            self.top_beads = []
            self.bottom_beads = []

            Color(.8, .8, .8, 1)

            for i in range(self.N_BARS):
                self.bar_rects.append([Rectangle(source='assets/graphics/silver.jpg'), Rectangle(source='assets/graphics/silver.jpg')])

                top = AbacusColumn(self.N_TOP_BEADS, self)
                self.add_widget(top)

                bottom = AbacusColumn(self.N_BOTTOM_BEADS, self)
                self.add_widget(bottom)

                self.top_beads.append(top)
                self.bottom_beads.append(bottom)

        self.anim_queue = deque([])

        self.clear_button_src = 'assets/graphics/clear.png'

        self.bind(pos=self.update, size=self.update)
        self.update()

    def update(self, *args):
        border_w = max(self.height / 20, self.MIN_BORDER_W)

        self.bar_w = self.MAX_BAR_W - max((800 - min(self.width, 2 * self.height)) / 800 * 10, 0)

        inner_w = self.width - 2 * border_w
        bead_w = min(
            (self.height - 3 * border_w) / (self.N_TOP_BEADS + 1 + self.N_BOTTOM_BEADS + 1) * 2,
            (inner_w - self.N_BARS * self.MIN_BEAD_SPACING) / self.N_BARS
        )

        offset_x = max(160, inner_w - (bead_w + self.MIN_BEAD_SPACING) * self.N_BARS) / 2
        abacus_w = self.width - 2 * offset_x
        inner_w -= 2 * offset_x

        bead_w = min(
            (self.height - 3 * border_w) / (self.N_TOP_BEADS + 1 + self.N_BOTTOM_BEADS + 1) * 2,
            (inner_w - self.N_BARS * self.MIN_BEAD_SPACING) / self.N_BARS
        )

        self.border[0].pos = (self.x + offset_x, self.y + self.height - border_w)
        self.border[0].size = (abacus_w, border_w)

        self.border[1].pos = (self.x + offset_x, self.y)
        self.border[1].size = (abacus_w, border_w)

        self.border[2].pos = (self.x + offset_x, self.y)
        self.border[2].size = (border_w, self.height)

        self.border[3].pos = (self.x + offset_x + abacus_w - border_w, self.y)
        self.border[3].size = (border_w, self.height)

        self.border_highlight[0].pos = (self.x + offset_x, self.y + self.height - border_w / 5)
        self.border_highlight[0].size = (abacus_w, border_w / 5)

        self.border_highlight[1].pos = (self.x + offset_x + border_w, self.y + 4 * border_w / 5)
        self.border_highlight[1].size = (inner_w, border_w / 5)

        div_y = (
            self.y + border_w + bead_w / 2 * self.N_BOTTOM_BEADS +
            self.y + self.height - border_w - bead_w / 2 * self.N_TOP_BEADS
        ) / 2 - border_w / 2

        self.divider.pos = (self.x + offset_x + border_w, div_y)
        self.divider.size = (inner_w, border_w)

        self.border_highlight[2].pos = (
            self.x + offset_x + border_w,
            div_y + border_w - border_w / 5
        )
        self.border_highlight[2].size = (inner_w, border_w / 5)

        for i in range(self.N_BARS):
            bar = self.bar_rects[i]
            spacing = inner_w / self.N_BARS

            space_offset = spacing / 2 + spacing * (self.N_BARS - i - 1)
            x = self.x + offset_x + border_w + space_offset - self.bar_w / 2

            bar[0].pos = (x, self.y + border_w - border_w / 10)
            bar[0].size = (self.bar_w, div_y - self.y - border_w + border_w / 10)

            bar[1].pos = (x, div_y + border_w - border_w / 10)
            bar[1].size = (
                self.bar_w,
                self.y + self.height - border_w - (div_y + border_w - border_w / 10)
            )

            bead_x = x + self.bar_w / 2 - bead_w / 2

            top_beads = self.top_beads[i]

            top_beads.size = (bead_w, self.y + self.height - div_y - border_w)
            top_beads.pos = (bead_x, div_y + border_w)

            bead_space = div_y - border_w - bead_w / 2 * self.N_BOTTOM_BEADS - self.y

            for j in range(len(top_beads.down)):
                bead = top_beads.down[j]

                anim_offset = floor(bead_space * bead.get_anim_offset())

                bead.pos = (
                    bead_x,
                    self.y + self.height - border_w - bead_w / 2 - (len(top_beads.down) - j - 1) * bead_w / 2 - anim_offset
                )
                bead.size = (bead_w, bead_w / 2)

            for j in range(len(top_beads.up)):
                bead = top_beads.up[j]

                anim_offset = floor(bead_space * bead.get_anim_offset())

                bead.pos = (
                    bead_x,
                    div_y + border_w + bead_w / 2 * (len(top_beads.up) - j - 1) + anim_offset
                )
                bead.size = (bead_w, bead_w / 2)

            bottom_beads = self.bottom_beads[i]

            bottom_beads.size = (bead_w, div_y - border_w - self.y)
            bottom_beads.pos = (bead_x, self.y + border_w)

            for j in range(len(bottom_beads.down)):
                bead = bottom_beads.down[j]

                anim_offset = floor(bead_space * bead.get_anim_offset())

                bead.pos = (
                    bead_x,
                    self.y + border_w + (len(bottom_beads.down) - j - 1) * bead_w / 2 + anim_offset
                )
                bead.size = (bead_w, bead_w / 2)

            for j in range(len(bottom_beads.up)):
                bead = bottom_beads.up[j]

                anim_offset = floor(bead_space * bead.get_anim_offset())

                bead.pos = (bead_x, div_y - bead_w / 2 * (len(bottom_beads.up) - j) - anim_offset)
                bead.size = (bead_w, bead_w / 2)

    def get_value(self):
        v = 0

        for i in range(self.N_BARS, 0, -1):
            i -= 1

            top_beads = self.top_beads[i]
            bottom_beads = self.bottom_beads[i]

            v += self.PLACE ** i * (len(top_beads.up) * self.TOP_V + len(bottom_beads.up))

        return v

    def set_value(self, v):
        Thread(target=self.preset(v)).start()

    def clear(self):
        Thread(target=self.reset()).start()

    def reset_abacus(self):
        for c in self.border + self.border_highlight + [self.divider]:
            self.canvas.remove(c)

        for c, d in self.bar_rects:
            self.canvas.remove(c)
            self.canvas.remove(d)

        for col in self.top_beads + self.bottom_beads:
            for bead in col.up + col.down:
                self.canvas.remove(bead)

        for w in self.top_beads + self.bottom_beads:
            self.remove_widget(w)

        self.__init__()        

    def update_top_beads(self, n):
        self.N_TOP_BEADS = n

        self.reset_abacus()

    def update_bottom_beads(self, n):
        self.N_BOTTOM_BEADS = n

        self.reset_abacus()

    def build_anim(self, anim):
        for col, n in anim.up_shifts:
            for bead in col.down[:n]:
                bead.anim = anim

        for col, n in anim.down_shifts:
            for bead in col.up[:n]:
                bead.anim = anim

        def f():
            for i in range(anim.speed):
                anim.progress += 1 / anim.speed

                self.update()

                sleep(self.ANIM_CLOCK_CYCLE)

            for col, n in anim.up_shifts:
                col.shift_up(n)

                for bead in col.up + col.down:
                    bead.anim = None

            for col, n in anim.down_shifts:
                col.shift_down(n)

                for bead in col.up + col.down:
                    bead.anim = None

            self.update()

        return f

    def enqueue_anim(self, anim):
        self.anim_queue.append(anim)

    def play_anims_from_queue(self):
        def f():
            while len(self.anim_queue) > 0:
                ta = Thread(target=self.anim_queue.popleft()())
                ta.start()
                ta.join()

                sleep(1)

        t = Thread(target=f)
        t.start()

    # animations

    def preset(self, x):
        anim = AbacusAnim()

        i = 0

        while x > 0:
            n = x % self.PLACE

            top = n // self.TOP_V
            bottom = n % self.TOP_V

            anim.add_shift_up(self.top_beads[i], top)
            anim.add_shift_up(self.bottom_beads[i], bottom)

            x //= self.PLACE

            i += 1

            if i > self.N_BARS:
                return False

        return self.build_anim(anim)

    def reset(self):
        anim = AbacusAnim()

        for i in range(self.N_BARS):
            if len(self.top_beads[i].up) > 0:
                anim.add_shift_down(self.top_beads[i], -1)

            if len(self.bottom_beads[i].up) > 0:
                anim.add_shift_down(self.bottom_beads[i], -1)

        return self.build_anim(anim)

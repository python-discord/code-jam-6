from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout


class Bead(Rectangle):
    def __init__(self, **kwargs):
        super(Bead, self).__init__(source='assets/graphics/bead.png', **kwargs)


class AbacusColumn:
    def __init__(self, n_beads):
        self.n_beads = n_beads
        self.up = []
        self.down = []

        for i in range(n_beads):
            self.down.append(Bead())

    def shift_up(self, n):
        if len(self.down) < n:
            return False

        for i in range(n):
            self.up.append(self.down.pop())

        return len(self.down)

    def shift_down(self, n):
        if len(self.up) < n:
            return False

        for i in range(n):
            self.down.append(self.up.pop())

        return len(self.up)


class Abacus(FloatLayout):
    MAX_BAR_W = 10
    MIN_BORDER_W = 16
    MAX_BEAD_SPACING = 8

    N_BARS = 12
    N_TOP_BEADS = 2
    N_BOTTOM_BEADS = 5

    def __init__(self, **kwargs):
        super(Abacus, self).__init__(**kwargs)

        self.bar_w = self.MAX_BAR_W

        with self.canvas:
            Color(1, 1, 1, 1)

            self.border = []

            for i in range(4):
                self.border.append(Rectangle(source='assets/graphics/wood.png'))

            Color(1, 1, 1, 0.2)

            self.border_highlight = [Rectangle(), Rectangle()]

            Color(1, 1, 1, 1)

            self.divider = Rectangle(source='assets/graphics/wood.png')

            Color(1, 1, 1, 0.2)

            self.border_highlight.append(Rectangle())

            self.bar_rects = []
            self.top_beads = []
            self.bottom_beads = []

            Color(0.8, 0.8, 0.8, 1)

            for i in range(self.N_BARS):
                self.bar_rects.append([Rectangle(), Rectangle()])

                self.top_beads.append(AbacusColumn(self.N_TOP_BEADS))
                self.bottom_beads.append(AbacusColumn(self.N_BOTTOM_BEADS))

            # temp tests

            self.top_beads[1].shift_up(1)

            print(self.get_value())

        self.bind(pos=self.update, size=self.update)
        self.update()

    def update(self, *args):
        border_w = max(self.height / 20, self.MIN_BORDER_W)

        self.bar_w = self.MAX_BAR_W - max((800 - min(self.width, 2 * self.height)) / 800 * 10, 0)

        inner_w = self.width - 2 * border_w
        bead_w = min(
            (self.height - 3 * border_w) / (self.N_TOP_BEADS + 1 + self.N_BOTTOM_BEADS + 1) * 2,
            (inner_w - self.N_BARS * self.MAX_BEAD_SPACING) / self.N_BARS
        )

        offset_x = max(0, inner_w - (bead_w + self.MAX_BEAD_SPACING) * self.N_BARS) / 2
        abacus_w = self.width - 2 * offset_x
        inner_w -= 2 * offset_x

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

            for j in range(len(top_beads.down)):
                top_beads.down[j].pos = (
                    bead_x,
                    self.y + self.height - border_w - bead_w / 2 - j * bead_w / 2
                )
                top_beads.down[j].size = (bead_w, bead_w / 2)

            for j in range(len(top_beads.up)):
                top_beads.up[j].pos = (
                    bead_x,
                    div_y + border_w + bead_w / 2 * (len(top_beads.up) - j - 1)
                )
                top_beads.up[j].size = (bead_w, bead_w / 2)

            bottom_beads = self.bottom_beads[i]

            for j in range(len(bottom_beads.down)):
                bottom_beads.down[j].pos = (bead_x, self.y + border_w + j * bead_w / 2)
                bottom_beads.down[j].size = (bead_w, bead_w / 2)

            for j in range(len(bottom_beads.up)):
                bottom_beads.up[j].pos = (bead_x, div_y - bead_w / 2 * (len(bottom_beads.up) - j))
                bottom_beads.up[j].size = (bead_w, bead_w / 2)

    def get_value(self):
        v = 0

        top_v = self.N_BOTTOM_BEADS + 1
        place = (self.N_TOP_BEADS + 1) * top_v

        for i in range(self.N_BARS, 0, -1):
            i -= 1

            top_beads = self.top_beads[i]
            bottom_beads = self.bottom_beads[i]

            v += place ** i * (len(top_beads.up) * top_v + len(bottom_beads.up))

        return v

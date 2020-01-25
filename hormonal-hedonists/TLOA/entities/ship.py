from TLOA.core.constants import LANE_BOUNDS
from TLOA.entities import MovingEntity


class BrownShip(MovingEntity):
    id = 'brown_ship'

    def __init__(self, lane_id, health=100, velocity=(-1, 0), **kwargs):
        super().__init__(health=health, velocity=velocity, **kwargs)
        self.lane_id = lane_id
        self.is_anchored = False

    def step(self, dt, game):
        if self.is_anchored:
            game.health -= 10
            self.health = 0
        else:
            x_stop = LANE_BOUNDS[self.lane_id][0]
            if self.shape.x > x_stop:
                super().step(dt, game)
            if self.shape.x <= x_stop:
                self.shape.x = x_stop
                self.is_anchored = True

    def __repr__(self):
        return f'{self.__class__.__name__}(lane_id={self.lane_id})'


class GoldenShip(BrownShip):
    id = 'golden_ship'

    def __init__(self, lane_id, velocity=(-0.5, 0), **kwargs):
        super().__init__(lane_id, velocity=velocity, **kwargs)

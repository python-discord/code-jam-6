import random
from typing import Tuple

from kivy.graphics.instructions import RenderContext, InstructionGroup

from primal.engine.perlin import sample
from primal.engine.sprite import Sprite, RotatableSprite


class World:
    RADIUS_WIDTH = 3
    RADIUS_HEIGHT = 3

    def __init__(self, pos: Tuple[float, float]):
        chunk_pos = World.get_chunk_coords_from_pos(pos)

        self.loaded_center = chunk_pos
        self.seed = random.randint(0, 2 ** 32 - 1)
        self.chunks = dict()

        self.loaded_chunks = [
            [None for _ in World.get_loaded_col_range(chunk_pos[0])]
            for _ in World.get_loaded_row_range(chunk_pos[1])
        ]

        self.chunk_instructions = [
            [InstructionGroup() for _ in World.get_loaded_col_range(chunk_pos[0])]
            for _ in World.get_loaded_row_range(chunk_pos[1])
        ]

        self.load_area(self.loaded_center)

    def update(self, pos: Tuple[float, float]):
        chunk_pos = World.get_chunk_coords_from_pos(pos)

        if chunk_pos == self.loaded_center:
            return

        self.loaded_center = chunk_pos
        self.load_area(chunk_pos)

    def draw(self, canvas: RenderContext):
        for row in self.chunk_instructions:
            for instruction in row:
                canvas.add(instruction)

    def load_area(self, pos: Tuple[int, int]):
        for index_y, y in enumerate(World.get_loaded_row_range(pos[1])):
            if y not in self.chunks:
                self.chunks[y] = dict()

            row_chunks = self.chunks[y]
            for index_x, x in enumerate(World.get_loaded_col_range(pos[0])):
                instruction_group = self.chunk_instructions[index_y][index_x]
                instruction_group.clear()

                if x not in row_chunks:
                    row_chunks[x] = Chunk((x * Chunk.SIZE, y * Chunk.SIZE), self.seed)

                self.loaded_chunks[index_y][index_x] = row_chunks[x]
                self.loaded_chunks[index_y][index_x].draw(instruction_group)

        for y in range(len(self.loaded_chunks)):
            for x in range(len(self.loaded_chunks[y])):
                self.loaded_chunks[y][x].draw_features(self.chunk_instructions[y][x])

    @staticmethod
    def get_loaded_row_range(y: int):
        return range(y - World.RADIUS_HEIGHT, y + World.RADIUS_HEIGHT + 1)

    @staticmethod
    def get_loaded_col_range(x: int):
        return range(x - World.RADIUS_WIDTH, x + World.RADIUS_WIDTH + 1)

    @staticmethod
    def get_chunk_coords_from_pos(pos: Tuple[float, float]) -> Tuple[int, int]:
        return int(pos[0] / Chunk.SIZE), int(pos[1] / Chunk.SIZE)


class Chunk:
    SIZE = 1000

    def __init__(self, pos: Tuple[int, int], seed: int):
        self.pos = pos
        self.sample = sample(pos[0] / 10000, pos[1] / 10000, seed=seed)
        self.items = set()
        self.chunk_features = set()

        if self.sample > 0.75:
            image = 'i.png'
            self.type = 3
        elif self.sample > 0.5:
            image = 'l.png'
            self.type = 2
        elif self.sample > 0.25:
            image = 's.png'
            self.type = 1
        else:
            image = 'w.png'
            self.type = 0

        self.terrain = Sprite(image, pos, (Chunk.SIZE, Chunk.SIZE))
        self.generate_terrain()

    def generate_terrain(self):
        if self.type == 0:
            return

        while random.randint(0, 1) == 1:
            s = random.randint(50, 100)
            angle = random.randint(0, 359)
            sprite = 'r.png'

            self.chunk_features.add(
                RotatableSprite(sprite, Chunk.get_random_position(self.pos), (s, s), angle))

        if self.type != 2:
            return

        while random.randint(0, 1) == 1:
            s = random.randint(50, 100)
            angle = random.randint(0, 359)
            sprite = 'topOfTree.png'

            self.chunk_features.add(
                RotatableSprite(sprite, Chunk.get_random_position(self.pos), (s, s), angle))

    def draw(self, group: InstructionGroup):
        self.terrain.draw(group)

    def draw_features(self, group: InstructionGroup):
        for feature in self.chunk_features:
            feature.draw(group)

    @staticmethod
    def get_random_position(pos):
        return pos[0] + random.randint(0, Chunk.SIZE), pos[1] + random.randint(0, Chunk.SIZE)

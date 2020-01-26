import random
from typing import Tuple, Set

from kivy.graphics.instructions import RenderContext, InstructionGroup

from primal.engine.perlin import sample
from primal.engine.sprite import Sprite
from primal.engine.feature import Feature


class World:
    RADIUS_WIDTH = 2
    RADIUS_HEIGHT = 2
    LOAD_RADIUS = 1

    def __init__(self, pos: Tuple[float, float]):
        self.world_group = InstructionGroup()
        self.top_group = InstructionGroup()

        chunk_pos = World.get_chunk_coords_from_pos(pos)

        self.loaded_center = chunk_pos
        self.seed = random.randint(0, 2 ** 32 - 1)
        self.chunks = dict()

        self.loaded_chunks = [
            [None for _ in World.get_loaded_range(chunk_pos[0], World.RADIUS_WIDTH)]
            for _ in World.get_loaded_range(chunk_pos[1], World.RADIUS_HEIGHT)
        ]

        size = Chunk.SIZE, Chunk.SIZE
        self.terrain_instructions = [
            [Sprite(None, (0, 0), size) for _ in
             World.get_loaded_range(chunk_pos[0], World.RADIUS_WIDTH)]
            for _ in World.get_loaded_range(chunk_pos[1], World.RADIUS_HEIGHT)
        ]

        self.features_chunk_instructions = [
            [InstructionGroup() for _ in World.get_loaded_range(chunk_pos[0], World.RADIUS_WIDTH)]
            for _ in World.get_loaded_range(chunk_pos[1], World.RADIUS_HEIGHT)
        ]

        self.top_features_chunk_instructions = [
            [InstructionGroup() for _ in World.get_loaded_range(chunk_pos[0], World.RADIUS_WIDTH)]
            for _ in World.get_loaded_range(chunk_pos[1], World.RADIUS_HEIGHT)
        ]

        for row in self.features_chunk_instructions:
            for instruction in row:
                self.world_group.add(instruction)

        self.load_area(self.loaded_center)

    def get_chunk_from_coords(self, pos):
        coords = self.get_chunk_coords_from_pos(pos)
        return self.chunks[coords[1]][coords[0]]

    def get_chunk_in_range(self, rng: int):
        for y in World.get_loaded_range(World.RADIUS_HEIGHT, rng):
            for x in World.get_loaded_range(World.RADIUS_WIDTH, rng):
                yield self.loaded_chunks[y][x]

    def update(self, pos: Tuple[float, float]):
        x, y = pos

        x, y = World.get_chunk_coords_from_pos((x, y))
        lx, ly = self.loaded_center

        if x + World.LOAD_RADIUS == lx or x - World.LOAD_RADIUS == lx or x == lx:
            if y + World.LOAD_RADIUS == ly or y - World.LOAD_RADIUS == ly or y == ly:
                return

        self.loaded_center = x, y
        self.load_area(self.loaded_center)

    def draw(self, canvas: RenderContext):
        for row in self.terrain_instructions:
            for terrain in row:
                terrain.draw(canvas)

        canvas.add(self.world_group)

    def draw_top(self, canvas: RenderContext):
        canvas.add(self.top_group)

    def render_chunk_at(self, x: int, y: int):
        instruction_group = self.features_chunk_instructions[y][x]
        self.world_group.remove(instruction_group)
        top_instruction_group = self.top_features_chunk_instructions[y][x]
        self.top_group.remove(top_instruction_group)

        instruction_group = InstructionGroup()
        self.features_chunk_instructions[y][x] = instruction_group
        self.world_group.add(instruction_group)

        top_instruction_group = InstructionGroup()
        self.top_features_chunk_instructions[y][x] = top_instruction_group
        self.top_group.add(top_instruction_group)
        self.loaded_chunks[y][x].draw_features(instruction_group, top_instruction_group)

    def render_chunk(self, chunk):
        for y in range(len(self.loaded_chunks)):
            for x in range(len(self.loaded_chunks[y])):
                if chunk == self.loaded_chunks[y][x]:
                    self.render_chunk_at(x, y)
                    return

    def load_area(self, pos: Tuple[int, int]):
        for index_y, y in enumerate(World.get_loaded_range(pos[1], World.RADIUS_HEIGHT)):
            if y not in self.chunks:
                self.chunks[y] = dict()

            row_chunks = self.chunks[y]
            for index_x, x in enumerate(World.get_loaded_range(pos[0], World.RADIUS_WIDTH)):
                if x not in row_chunks:
                    row_chunks[x] = Chunk((x * Chunk.SIZE, y * Chunk.SIZE), self.seed)

                terrain_instruction = self.terrain_instructions[index_y][index_x]
                self.loaded_chunks[index_y][index_x] = row_chunks[x]
                self.loaded_chunks[index_y][index_x].draw(terrain_instruction)
                self.render_chunk_at(index_x, index_y)

    @staticmethod
    def get_loaded_range(x: int, rng: int):
        return range(x - rng, x + rng + 1)

    @staticmethod
    def get_chunk_coords_from_pos(pos: Tuple[float, float]) -> Tuple[int, int]:
        x, y = pos
        if x < 0:
            x -= Chunk.SIZE
        if y < 0:
            y -= Chunk.SIZE

        return int(x / Chunk.SIZE), int(y / Chunk.SIZE)


class Chunk:
    SIZE = 1000

    def __init__(self, pos: Tuple[int, int], seed: int):
        self.pos = pos
        self.sample = sample(pos[0] / 10000, pos[1] / 10000, seed=seed)
        self.items = set()
        self.chunk_features = set()

        if self.sample > 0.75:
            self.image = 'i.png'
            self.type = 3
        elif self.sample > 0.5:
            self.image = 'l.png'
            self.type = 2
        elif self.sample > 0.25:
            self.image = 's.png'
            self.type = 1
        else:
            self.image = 'w.png'
            self.type = 0

        self.generate_terrain()

    def generate_terrain(self):
        if self.type == 0:
            return

        while random.randint(0, 1) == 1:
            s = random.randint(100, 150)
            angle = 0
            sprite = 'r.png'
            rock = Feature(sprite, Chunk.get_random_position(self.pos, s), .0,
                           (s, s), angle, 'rock', True)
            rock.feature.set_angle(random.randint(0, 360))
            self.chunk_features.add(rock)

        if self.type != 2:
            return

        bushes = ['bushBB.png', 'bushBO.png', 'bushBP.png', 'bushBR.png', 'bushBY.png']
        while random.randint(0, 1) != 1:
            s = 65
            angle = random.randint(0, 359)
            sprite = random.choice(bushes)
            type = sprite.replace('.png', '')
            self.chunk_features.add(
                Feature(sprite, Chunk.get_random_position(self.pos, s), 1.0, (s, s), angle, type))

        while random.randint(0, 3) != 1:
            s = random.randint(150, 280)
            angle = random.randint(0, 359)
            sprite = 'topOfTree.png'

            self.chunk_features.add(
                Feature(sprite, Chunk.get_random_position(self.pos, s), 2.0, (s, s), angle, 'tree'))

    def draw(self, terrain: Sprite):
        terrain.set_position(self.pos)
        terrain.set_source(self.image)

    def sort_key(self, f: Feature):
        return f.get_z()

    def draw_features(self, group: InstructionGroup, top_group: InstructionGroup):
        list = sorted(self.chunk_features, key=self.sort_key)

        for feature in list:
            if feature.get_z() >= 2.0:
                feature.draw(top_group)
            else:
                feature.draw(group)

    def get_features(self) -> Set[Feature]:
        return self.chunk_features

    def remove_feature(self, feature: Feature):
        self.chunk_features.discard(feature)

    @staticmethod
    def get_random_position(pos, size):
        return (
            pos[0] + random.randint(0, Chunk.SIZE - size),
            pos[1] + random.randint(0, Chunk.SIZE - size),
        )

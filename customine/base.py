# -*- coding: utf-8 -*-

import mclevel
from box import BoundingBox


class BaseBuilder(object):
    DIRECTIONS = {
        'SOUTH': 0,
        'WEST': 1,
        'NORTH': 2,
        'EAST': 3,
    }
    VERTICAL_DIRECTIONS = {
        'UP': 4,
        'DOWN': 5
    }

    def __init__(self, level_path, init_pos=None, size=[1, 1, 1]):
        super(BaseBuilder, self).__init__()
        self.level = None
        self.level_path = level_path
        self.init_pos = init_pos
        self.size = size

    def load_level(self, level_path=None):
        "load the level using `self.level_path` or set a new one and load it"
        if level_path is not None:
            self.level_path = level_path

        if self.level_path is None:
            return

        self.level = mclevel.fromFile(self.level_path)
        return self.level

    def prepare_stage(self):
        """
        ensure chunks in given size, considering init_pos, do exist
        and their chunk positions (also set as `self.chunk_positions`)
        """
        if self.init_pos is None or self.level is None:
            return

        x, y, z = self.init_pos

        bbox = BoundingBox(origin=(x, y, z), size=self.size)
        chunk_positions = bbox.chunkPositions
        self.level.createChunksInBox(bbox)
        self.chunk_positions = chunk_positions
        return chunk_positions

    def prepare_all(self):
        "load level and prepare stage"
        self.load_level()
        self.prepare_stage()

    def generate(self):
        pass

    def change_block_at(self, x, y, z, block_id, block_data):
        self.level.setBlockAt(x, y, z, block_id)
        self.level.setBlockDataAt(x, y, z, block_data)

    def save(self):
        "mark chunks used as changed, regenerate the lights, and save level"
        for chunk_pos in self.chunk_positions:
            chunk = self.level.getChunk(chunk_pos[0], chunk_pos[1])
            chunk.chunkChanged()

        self.level.generateLights()
        self.level.saveInPlace()

    @classmethod
    def get_new_vect_as_sum(cls, k, w):
        "return the sum of vect K and W as a new vetor"
        return map(sum, zip(k, w))

    @classmethod
    def get_vect_mult(cls, vect, amount):
        """
        multiply each value of vect by the amount, and return it as a new vect
        """
        return [i * amount for i in vect]

    @classmethod
    def get_direction_vect(cls, direction):
        "return the directions vector"

        dir_vect = [0, 0, 0]
        # From NORTH to SOUTH (+Z)
        if direction == cls.DIRECTIONS['SOUTH']:
            dir_vect[2] = 1
        # From EAST to WEST (-X)
        if direction == cls.DIRECTIONS['WEST']:
            dir_vect[0] = -1
        # From WEST to EAST (+X)
        if direction == cls.DIRECTIONS['EAST']:
            dir_vect[0] = 1
        # From SOUTH to NORTH (-Z)
        if direction == cls.DIRECTIONS['NORTH']:
            dir_vect[2] = -1
        # From DOWN to UP (+Y)
        if direction == cls.VERTICAL_DIRECTIONS['UP']:
            dir_vect[1] = 1
        # FROM UP to DOWN (-Y)
        if direction == cls.VERTICAL_DIRECTIONS['DOWN']:
            dir_vect[1] = -1

        return dir_vect

    @classmethod
    def get_direction_vect_mult(cls, direction, amount):
        """
        get a new direction vector multiplied by amount (in each value)
        """
        return cls.get_vect_mult(
            cls.get_direction_vect(direction),
            amount
        )

    @classmethod
    def get_90_degrees_from_direction(cls, direction):
        """
        Return a new direction vector turned 90+ degrees from a given direction
        """
        return cls.get_n90_degrees_from_direction(direction, n=1)

    @classmethod
    def get_n90_degrees_from_direction(cls, direction, n=1):
        """
        Return a new direction vector turned x * 90+ degrees from a given direction,
        n as default is 1
        """
        return (direction + n) % 4
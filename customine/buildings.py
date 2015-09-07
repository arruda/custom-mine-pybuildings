# -*- coding: utf-8 -*-

from .base import BaseBuilder
from .mixins import MultiBlockCorridorMixin, MultiBlockRoomMixin


class Castle(BaseBuilder, MultiBlockCorridorMixin):

    OUTER_WALL = {
        'block_id': 2504,
        'block_data': 3
    }
    LEFT_WALL = {
        'block_id': 2504,
        'block_data': 3
    }
    RIGHT_WALL = {
        'block_id': 2504,
        'block_data': 4
    }
    GROUD = {
        'block_id': 2504,
        'block_data': 5
    }
    CEALING = {
        'block_id': 2504,
        'block_data': 6
    }

    def __init__(self, level_path, init_pos=None):
        super(Castle, self).__init__(level_path, init_pos=init_pos)
        self.size = [10, 10, 10]

    def generate(self, direction):
        x, y, z = self.init_pos
        lengh = 5
        width = 4
        height = 3
        # self.gen_single_block_room(
        #     self.init_pos,
        #     lengh,
        #     width,
        #     height,
        #     self.OUTER_WALL['block_id'],
        #     self.OUTER_WALL['block_data'],
        #     direction=direction
        # )

        blocks_info = {
            'left_wall_info': self.LEFT_WALL,
            'right_wall_info': self.RIGHT_WALL,
            'ground_info': self.GROUD,
            'cealing_info': self.CEALING,
            'direction': direction
        }
        self.gen_multi_block_corridor(
            self.init_pos,
            lengh,
            width,
            height,
            **blocks_info
        )


class Tower(BaseBuilder, MultiBlockRoomMixin):

    def __init__(self, level_path, init_pos=None, num_floors=3):
        super(Tower, self).__init__(level_path, init_pos=init_pos)
        self.num_floors = num_floors

    def generate(self, direction):
        x, y, z = self.init_pos
        length = 6
        width = 6
        height = 3

        new_pos = self.init_pos
        for i in xrange(0, self.num_floors):

            last_pos = self.gen_multi_block_room(
                list(new_pos),
                length=length,
                width=width,
                height=height
            )
            new_pos = self.get_new_vect_as_sum(
                new_pos,
                self.get_direction_vect_mult(
                    self.VERTICAL_DIRECTIONS['UP'],
                    height + 2
                )
            )

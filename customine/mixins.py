# -*- coding: utf-8 -*-

# import mclevel
# from box import BoundingBox

from .base import BaseBuilder


class WallMixin(object):

    def gen_wall(self, pos, length, height, block_id, block_data, direction=BaseBuilder.DIRECTIONS['SOUTH']):

        init_x, init_y, init_z = pos
        x, y, z = pos
        # walk along the length building up
        for i in xrange(length):
            new_direction_increased = self.get_direction_vect_mult(direction, i)
            x, y, z = self.get_new_vect_as_sum(
                pos,
                new_direction_increased
            )
            # increases Y+k
            for k in xrange(height):
                y = init_y + k
                self.change_block_at(x, y, z, block_id, block_data)
        return [x, y, z]


class GroundMixin(object):

    def gen_ground(self, pos, length, width, block_id, block_data, direction=BaseBuilder.DIRECTIONS['SOUTH']):

        init_x, init_y, init_z = pos
        x, y, z = pos

        # walk along the length building to the width
        for i in xrange(length):
            length_direction_increased = self.get_direction_vect_mult(direction, i)
            x, y, z = self.get_new_vect_as_sum(
                pos,
                length_direction_increased
            )
            # increases width with k in +90º from direction
            for k in xrange(width):
                direction_90_degrees = self.get_90_degrees_from_direction(direction)
                width_direction_increased = self.get_direction_vect_mult(direction_90_degrees, k)

                x1, y1, z1 = self.get_new_vect_as_sum(
                    [x, y, z],
                    width_direction_increased
                )
                self.change_block_at(x1, y1, z1, block_id, block_data)
        return [x1, y1, z1]


class SingleBlockCorridorMixin(WallMixin, GroundMixin):

    def gen_single_block_corridor(self,
                                  pos,
                                  length,
                                  width,
                                  height,
                                  block_id,
                                  block_data,
                                  direction=BaseBuilder.DIRECTIONS['SOUTH']):

        pos[1] = pos[1] - 1
        # create a ground in the floor, going to the given direction
        after_ground_pos = self.gen_ground(pos, length, width, block_id, block_data, direction)

        right_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_90_degrees_from_direction(direction), width
            )
        )

        after_right_wall_pos = self.gen_wall(right_wall_pos, length, height + 2, block_id, block_data, direction)

        left_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_n90_degrees_from_direction(direction, n=3), 1
            )
        )

        after_left_wall_pos = self.gen_wall(left_wall_pos, length, height + 2, block_id, block_data, direction)

        cealing_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.VERTICAL_DIRECTIONS['UP'],
                height + 1
            )
        )
        after_cealing_pos = self.gen_ground(cealing_pos, length, width, block_id, block_data, direction)

        return after_cealing_pos


class MultiBlockCorridorMixin(WallMixin, GroundMixin):

    def gen_multi_block_corridor(self,
                                 pos,
                                 length,
                                 width,
                                 height,
                                 left_wall_info=None,
                                 right_wall_info=None,
                                 ground_info=None,
                                 cealing_info=None,
                                 direction=BaseBuilder.DIRECTIONS['SOUTH']):

        pos[1] = pos[1] - 1
        # create a ground in the floor, going to the given direction
        after_ground_pos = self.gen_ground(pos, length, width, ground_info['block_id'], ground_info['block_data'], direction)

        right_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_90_degrees_from_direction(direction), width
            )
        )

        after_right_wall_pos = self.gen_wall(right_wall_pos, length, height + 2, right_wall_info['block_id'], right_wall_info['block_data'], direction)

        left_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_n90_degrees_from_direction(direction, n=3), 1
            )
        )

        after_left_wall_pos = self.gen_wall(left_wall_pos, length, height + 2, left_wall_info['block_id'], left_wall_info['block_data'], direction)

        cealing_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.VERTICAL_DIRECTIONS['UP'],
                height + 1
            )
        )
        after_cealing_pos = self.gen_ground(cealing_pos, length, width, cealing_info['block_id'], cealing_info['block_data'], direction)

        return after_cealing_pos


class MultiBlockRoomMixin(WallMixin, GroundMixin):

    FACE_WALL = {
        'block_id': 2504,
        'block_data': 1
    }
    BACK_WALL = {
        'block_id': 2504,
        'block_data': 2
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
        'block_data': 15
    }
    CEALING = {
        'block_id': 2504,
        'block_data': 6
    }

    def __init__(self, blocks_info={}):
        if 'FACE_WALL' in blocks_info:
            self.FACE_WALL = blocks_info.pop('FACE_WALL')

        if 'BACK_WALL' in blocks_info:
            self.BACK_WALL = blocks_info.pop('BACK_WALL')

        if 'LEFT_WALL' in blocks_info:
            self.LEFT_WALL = blocks_info.pop('LEFT_WALL')

        if 'RIGHT_WALL' in blocks_info:
            self.RIGHT_WALL = blocks_info.pop('RIGHT_WALL')

        if 'GROUD' in blocks_info:
            self.GROUD = blocks_info.pop('GROUD')

        if 'CEALING' in blocks_info:
            self.CEALING = blocks_info.pop('CEALING')

    def gen_multi_block_room(self,
                             pos,
                             length,
                             width,
                             height,
                             direction=BaseBuilder.DIRECTIONS['SOUTH']):

        # length = 6
        # width = 6

        pos[0] = pos[0] - 1
        pos[1] = pos[1] - 1
        # create a ground in the floor, going to the given direction
        after_ground_pos = self.gen_ground(
            pos,
            length,
            width,
            self.GROUD['block_id'],
            self.GROUD['block_data'],
            direction
        )

        right_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_90_degrees_from_direction(direction), width
            )
        )
        after_right_wall_pos = self.gen_wall(
            right_wall_pos,
            length,
            height + 2,
            self.RIGHT_WALL['block_id'],
            self.RIGHT_WALL['block_data'],
            direction
        )

        left_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_n90_degrees_from_direction(direction, n=3), 1
            )
        )

        after_left_wall_pos = self.gen_wall(
            left_wall_pos,
            length,
            height + 2,
            self.LEFT_WALL['block_id'],
            self.LEFT_WALL['block_data'],
            direction
        )

        face_wall_direction = self.get_90_degrees_from_direction(direction)

        face_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.get_90_degrees_from_direction(face_wall_direction),
                1
            )
        )
        after_face_wall_pos = self.gen_wall(
            face_wall_pos,
            length,
            height + 2,
            self.FACE_WALL['block_id'],
            self.FACE_WALL['block_data'],
            face_wall_direction
        )
        back_wall_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                direction,
                length
            )
        )
        back_wall_direction = face_wall_direction

        after_back_wall_pos = self.gen_wall(
            back_wall_pos,
            length,
            height + 2,
            self.BACK_WALL['block_id'],
            self.BACK_WALL['block_data'],
            back_wall_direction
        )

        cealing_pos = self.get_new_vect_as_sum(
            pos,
            self.get_direction_vect_mult(
                self.VERTICAL_DIRECTIONS['UP'],
                height + 1
            )
        )
        after_cealing_pos = self.gen_ground(
            cealing_pos,
            length,
            width,
            self.CEALING['block_id'],
            self.CEALING['block_data'],
            direction
        )
        return after_cealing_pos

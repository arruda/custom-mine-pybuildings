#!/usr/bin/env python
# -*- coding: utf-8 -*-

from customine.base import BaseBuilder
from customine.buildings import Castle, Tower


def testando(block_id=2504, block_data=15):
    level_path = "/home/arruda/.minecraft_galera/saves/testando/level.dat"
    init_pos = [-269, 4, 1584]
    size = [4, 4, 4]
    x, y, z = init_pos
    b = BaseBuilder(level_path, init_pos=init_pos, size=size)
    b.load_level()
    b.prepare_stage()

    # block_id = 2504
    # block_data = 15

    b.change_block_at(x, y, z, block_id, block_data)

    b.save()
    return b


def castelo(direction=BaseBuilder.DIRECTIONS['SOUTH']):
    level_path = "/home/arruda/.minecraft_galera/saves/testando/level.dat"
    init_pos = [-40, 74, 185]
    castle = Castle(level_path, init_pos=init_pos)
    castle.prepare_all()
    castle.generate(direction=direction)
    castle.save()
    return castle


def torre(direction=BaseBuilder.DIRECTIONS['SOUTH']):
    level_path = "/home/arruda/.minecraft_galera/saves/testando/level.dat"
    init_pos = [-39, 77, 188]
    tower = Tower(level_path, init_pos=init_pos)
    tower.prepare_all()
    tower.generate(direction=direction)
    tower.save()
    return tower


if __name__ == '__main__':
    torre()

# -*- coding: utf-8 -*-

import os

from mock import patch, Mock, MagicMock
import unittest

import mclevel
import box

import customine.base
from customine.base import BaseBuilder


class TestBaseBuilder(unittest.TestCase):

    def setUp(self):
        pass

    @patch.object(mclevel, 'fromFile', Mock(return_value='some_level'))
    def test_load_level_should_set_level_if_self_is_none(self):
        level_path = "path_to_lvl.dat"
        # init_pos = [-269, 4, 1584]
        # size = [4, 4, 4]
        # x, y, z = init_pos
        b = BaseBuilder(level_path=None)
        level = b.load_level(level_path)

        self.assertEquals(b.level_path, level_path)
        self.assertEquals(level, 'some_level')

    @patch.object(mclevel, 'fromFile', Mock(return_value='some_level'))
    def test_load_level_should_return_none_if_no_level_path_is_set(self):
        b = BaseBuilder(level_path=None)
        level = b.load_level()

        self.assertEquals(level, None)

    @patch.object(mclevel, 'fromFile', Mock(return_value='some_level'))
    def test_call_mclevel_fromFile_with_level_path(self):
        level_path = "path_to_lvl.dat"
        b = BaseBuilder(level_path=level_path)
        level = b.load_level()

        self.assertEquals(level, 'some_level')
        mclevel.fromFile.assert_called_once_with(level_path)

    def test_prepare_stage_should_return_none_if_no_init_pos_or_level_is_set(self):
        init_pos = [-269, 4, 1584]
        b = BaseBuilder(level_path=None, init_pos=init_pos)

        ret = b.prepare_stage()
        self.assertEquals(ret, None)

        b = BaseBuilder(level_path=None, init_pos=None)
        b.level = "loaded_level"

        ret = b.prepare_stage()
        self.assertEquals(ret, None)

    @patch('customine.base.BoundingBox', Mock())
    def test_prepare_stage_should_instantiate_box_with_correct_sizes_and_origin(self):
        init_pos = [1, 2, 3]
        size = [6, 5, 4]
        bb = BaseBuilder(level_path=None, init_pos=init_pos, size=size)

        #mocks
        customine.base.BoundingBox.return_value.chunkPositions = 'chunk_positions'
        bb.level = Mock()
        bb.level.createChunksInBox = Mock()

        ret_chunks = bb.prepare_stage()
        self.assertEquals(ret_chunks, 'chunk_positions')
        customine.base.BoundingBox.assert_called_once_with(
            origin=tuple(init_pos), size=size
        )

    @patch('customine.base.BaseBuilder.load_level', Mock())
    @patch('customine.base.BaseBuilder.prepare_stage', Mock())
    def test_prepare_all_should_load_level_and_prepare_stage(self):
        bb = BaseBuilder(level_path=None)
        bb.prepare_all()
        BaseBuilder.load_level.assert_called_once_with()
        BaseBuilder.prepare_stage.assert_called_once_with()

    def test_change_block_at_should_change_id_and_data_correctly(Self):
        bb = BaseBuilder(level_path=None)

        x, y, z = [1, 2, 3]
        block_id = 'id'
        block_data = 'data'

        bb.level = Mock()
        bb.level.setBlockAt = Mock()
        bb.level.setBlockDataAt = Mock()

        bb.change_block_at(x=x, y=y, z=z, block_id=block_id, block_data=block_data)

        bb.level.setBlockAt.assert_called_once_with(x, y, z, block_id)
        bb.level.setBlockDataAt.assert_called_once_with(x, y, z, block_data)


    def tearDown(self):
        # ensure the file locks are closed
        # self.test_level.close()
        pass

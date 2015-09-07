# -*- coding: utf-8 -*-

import os

from mock import patch, Mock
import unittest

import mclevel

from box import BoundingBox

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

    def tearDown(self):
        # ensure the file locks are closed
        # self.test_level.close()
        pass

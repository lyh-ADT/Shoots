import unittest
from unittest.mock import patch
from random import Random

from ..bin.map_builder import MapBuilder

class TestMapBuilderInitMapMethod(unittest.TestCase):
    def test_init_map_odd_size(self):
        m = MapBuilder(5)
        m.init_map()
        expected = [
            [m.UNSET, m.WALL, m.UNSET, m.WALL, m.UNSET],
            [m.WALL, m.WALL, m.WALL, m.WALL, m.WALL],
            [m.UNSET, m.WALL, m.UNSET, m.WALL, m.UNSET],
            [m.WALL, m.WALL, m.WALL, m.WALL, m.WALL],
            [m.UNSET, m.WALL, m.UNSET, m.WALL, m.UNSET]
        ]

        self.assertListEqual(expected, m.map)

    def test_init_map_even_size(self):
        m = MapBuilder(4)
        m.init_map()
        expected = [
            [m.UNSET, m.WALL, m.UNSET, m.WALL],
            [m.WALL, m.WALL, m.WALL, m.WALL],
            [m.UNSET, m.WALL, m.UNSET, m.WALL],
            [m.WALL, m.WALL, m.WALL, m.WALL]
        ]

        self.assertListEqual(expected, m.map)


class TestMapBuilderSearchMethod(unittest.TestCase):
    def setUp(self):
        self.random = Random(0)

    @patch('Shoots.bin.map_builder.random')
    def test_dfs(self, random):
        random.choice._mock_side_effect = self.random.choice
        m = MapBuilder(5)
        m.build_dfs()
        expected = [
            [m.ROAD,m.ROAD,m.ROAD,m.ROAD,m.ROAD],
            [m.WALL,m.WALL,m.WALL,m.WALL,m.ROAD],
            [m.ROAD,m.ROAD,m.ROAD,m.ROAD,m.ROAD],
            [m.ROAD,m.WALL,m.WALL,m.WALL,m.WALL],
            [m.ROAD,m.ROAD,m.ROAD,m.ROAD,m.ROAD]
        ]
        self.assertListEqual(expected, m.map)
    
    @patch('Shoots.bin.map_builder.random')
    def test_bfs(self, random):
        random.choice._mock_side_effect = self.random.choice
        m = MapBuilder(5)
        m.build_bfs()
        expected = [
            [m.ROAD,m.ROAD,m.ROAD,m.ROAD,m.ROAD],
            [m.WALL,m.WALL,m.WALL,m.WALL,m.ROAD],
            [m.ROAD,m.ROAD,m.ROAD,m.ROAD,m.ROAD],
            [m.ROAD,m.WALL,m.ROAD,m.WALL,m.ROAD],
            [m.ROAD,m.ROAD,m.ROAD,m.WALL,m.ROAD]
        ]
        self.assertListEqual(expected, m.map)


if __name__ == "__main__":
    unittest.main()
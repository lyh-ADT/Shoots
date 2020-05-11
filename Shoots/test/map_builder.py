import unittest
from unittest.mock import patch
from random import Random

from ..bin.map import Map
from ..bin.map_builder import MapBuilder

class TestMapBuilderInitMapMethod(unittest.TestCase):
    def test_init_map_odd_size(self):
        m = MapBuilder(5)
        m.init_map()
        expected = [
            [Map.UNSET, Map.WALL, Map.UNSET, Map.WALL, Map.UNSET],
            [Map.WALL, Map.WALL, Map.WALL, Map.WALL, Map.WALL],
            [Map.UNSET, Map.WALL, Map.UNSET, Map.WALL, Map.UNSET],
            [Map.WALL, Map.WALL, Map.WALL, Map.WALL, Map.WALL],
            [Map.UNSET, Map.WALL, Map.UNSET, Map.WALL, Map.UNSET]
        ]

        self.assertListEqual(expected, m.map)

    def test_init_map_even_size(self):
        m = MapBuilder(4)
        m.init_map()
        expected = [
            [Map.UNSET, Map.WALL, Map.UNSET, Map.WALL],
            [Map.WALL, Map.WALL, Map.WALL, Map.WALL],
            [Map.UNSET, Map.WALL, Map.UNSET, Map.WALL],
            [Map.WALL, Map.WALL, Map.WALL, Map.WALL]
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
            [Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD],
            [Map.WALL,Map.WALL,Map.WALL,Map.WALL,Map.ROAD],
            [Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD],
            [Map.ROAD,Map.WALL,Map.WALL,Map.WALL,Map.WALL],
            [Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD]
        ]
        self.assertListEqual(expected, m.map)
    
    @patch('Shoots.bin.map_builder.random')
    def test_bfs(self, random):
        random.choice._mock_side_effect = self.random.choice
        m = MapBuilder(5)
        m.build_bfs()
        expected = [
            [Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD],
            [Map.WALL,Map.WALL,Map.WALL,Map.WALL,Map.ROAD],
            [Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD,Map.ROAD],
            [Map.ROAD,Map.WALL,Map.ROAD,Map.WALL,Map.ROAD],
            [Map.ROAD,Map.ROAD,Map.ROAD,Map.WALL,Map.ROAD]
        ]
        self.assertListEqual(expected, m.map)


if __name__ == "__main__":
    unittest.main()
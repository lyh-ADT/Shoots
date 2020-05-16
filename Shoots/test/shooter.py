import unittest

from Shoots.bin.map import Map
from Shoots.bin.shooter import Shooter
from Shoots.bin.info import Info

class TestCanSeeMethod(unittest.TestCase):
    def test_vertical(self):
        m = Map(2)
        m.map = [
            [Map.ROAD, Map.ROAD],
            [Map.ROAD, Map.ROAD]
        ]
        s1 = Shooter(m)
        s2 = Shooter(m)

        s1.position = (0, 0)
        s1.face = Info.FACE_DONW
        s2.position = (1, 0)
        s2.face = Info.FACE_LEFT

        self.assertTrue(s1.can_see(s2))
        self.assertFalse(s2.can_see(s1))

    def test_horizon(self):
        m = Map(2)
        m.map = [
            [Map.ROAD, Map.ROAD],
            [Map.ROAD, Map.ROAD]
        ]
        s1 = Shooter(m)
        s2 = Shooter(m)

        s1.position = (0, 0)
        s1.face = Info.FACE_RIGHT
        s2.position = (0, 1)
        s2.face = Info.FACE_DONW

        self.assertTrue(s1.can_see(s2))
        self.assertFalse(s2.can_see(s1))
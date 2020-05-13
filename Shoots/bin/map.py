from copy import deepcopy
import random

class Map:
    WALL = 0
    ROAD = 1
    UNSET = 2
    def __init__(self, size):
        from Shoots.bin.map_builder import MapBuilder
        self.size = size
        mb = MapBuilder(size)
        self.map = mb.build_bfs()

    def location_valid(self, loc):
        return (0 <= loc[0] and loc[0] < self.size) and (0 <= loc[1] and loc[1] < self.size)

    def is_road(self, loc):
        if self.location_valid(loc):
            return self.map[loc[0]][loc[1]] == Map.ROAD
        return False

    def get_view(self):
        return deepcopy(self.map)

    def spawn(self):
        pos = (-1, -1)
        while not self.is_road(pos):
            pos = (
                random.randint(0, self.size-1),
                random.randint(0, self.size-1)
            )
        return pos

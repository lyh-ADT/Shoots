from Shoots.bin.map_builder import MapBuilder

class Info:
    FACE_UP = 0
    FACE_DONW = 1
    FACE_LEFT = 2
    FACE_RIGHT = 3
    def __init__(self):
        self.sound = []
        self.shooter = []


class Map:
    def __init__(self, size):
        self.size = size
        mb = MapBuilder(size)
        self.map = mb.build_bfs()

    def location_valid(self, loc):
        return (0 <= loc[0] and loc[0] < self.size) and (0 <= loc[1] and loc[1] < self.size)
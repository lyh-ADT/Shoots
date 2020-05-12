from copy import deepcopy


class Info:
    FACE_UP = 0
    FACE_DONW = 1
    FACE_LEFT = 2
    FACE_RIGHT = 3
    def __init__(self):
        self.sound = []
        self.shooter = []
    
    def get_dict(self):
        return {
            'sound':self.sound,
            'shooter':self.shooter
        }


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
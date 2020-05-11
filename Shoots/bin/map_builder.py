from Shoots.bin.map import Map
import random

def print_map(m):
    for i in m:
        for j in i:
            print(j, end='')
        print()

class MapBuilder:
    # https://zhuanlan.zhihu.com/p/27381213

    def __init__(self, size):
        self.size = size
        self.map = []
        self.candidate = []
        self.path = []

    def build_dfs(self):
        '''
        build the map using dfs
        bfs better than dfs normally
        '''
        self.init_map()
        self.path = [(0,0)]
        self.dfs()

    def build_bfs(self):
        '''
        build the map using bfs
        bfs better than dfs normally
        '''
        self.init_map()
        self.path = []
        self.candidate = []
        self.bfs((0,0))

    def init_map(self):
        self.map = []
        c = [Map.UNSET, Map.WALL]
        for x in range(self.size):
            if x % 2 == 0:
                row = []
                for y in range(self.size):
                    row.append(c[y%2])
                
            else:
                row = [Map.WALL] * self.size
            self.map.append(row)

    def dfs(self):
        if len(self.path) <= 0:
            return

        cur = self.path[-1]
        self.candidate = self.get_sibling_unset(cur)

        if len(self.candidate) <= 0:
            self.path.pop()
            return self.dfs()

        choose = random.choice(self.candidate)
        if not self.location_is_unset(choose):
            raise AssertionError("should not have wall/road in candidate")
        self.connect_two_road(choose, cur)
        self.path.append(choose)
        return self.dfs()

    def bfs(self, cur):
        self.candidate.extend(self.get_sibling_unset(cur))

        if len(self.candidate) <= 0:
            return

        choose = random.choice(self.candidate)
        self.candidate.remove(choose)
        
        self.connect_to_sibling_road(choose)
        return self.bfs(choose)

    def connect_two_road(self, loc1, loc2):
        if loc1[0] == loc2[0]:
            # x equaled
            x = loc1[0]
            y = round((loc1[1] + loc2[1]) / 2)
        else:
            x = round((loc1[0] + loc2[0]) / 2)
            y = loc1[1]
        self.map[loc1[0]][loc1[1]] = Map.ROAD
        self.map[loc2[0]][loc2[1]] = Map.ROAD
        self.map[x][y] = Map.ROAD

    def location_valid(self, loc):
        return (0 <= loc[0] and loc[0] < self.size) and (0 <= loc[1] and loc[1] < self.size)

    def location_is_unset(self, loc):
        if self.location_valid(loc):
            return self.map[loc[0]][loc[1]] == Map.UNSET
        return False
    
    def location_is_road(self, loc):
        if self.location_valid(loc):
            return self.map[loc[0]][loc[1]] == Map.ROAD
        return False

    def get_sibling_unset(self, loc):
        dis = 2
        candidate = [
            (loc[0]-dis, loc[1]),
            (loc[0]+dis, loc[1]),
            (loc[0], loc[1]-dis),
            (loc[0], loc[1]+dis)
        ]
        roads = []
        for i in candidate:
            if self.location_is_unset(i):
                roads.append(i)
        return roads
    
    def get_sibling_roads(self, loc):
        dis = 2
        candidate = [
            (loc[0]-dis, loc[1]),
            (loc[0]+dis, loc[1]),
            (loc[0], loc[1]-dis),
            (loc[0], loc[1]+dis)
        ]
        roads = []
        for i in candidate:
            if self.location_is_road(i):
                roads.append(i)
        return roads

    def connect_to_sibling_road(self, loc):
        roads = self.get_sibling_roads(loc)
        if len(roads) == 0:
            roads.append(loc)
        loc2 = random.choice(roads)
        self.connect_two_road(loc, loc2)


if __name__ == "__main__":
    m = MapBuilder(15)
    m.build_bfs()
    print_map(m.map)
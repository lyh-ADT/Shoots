from Shoots.bin.map import Map
from Shoots.bin.info import Info

class Shooter:
    def __init__(self, map:Map):
        self.face = Info.FACE_UP # the direction of shooter's face
        self.vision = 5 # vision radius
        self.listen = 10 # listen radius
        self.cd = 3 # shot cool down tick
        self.cd_count = 0
        self.info = Info() # infomation of environment(sound, vision)
        self.map = map
        self.position = self.map.spawn()
    
    def update_info(self, info:Info):
        self.info = info
    
    def get_info(self):
        return self.info

    def shoot(self):
        if self.cd_count > 0:
            return
    
    def move_up(self):
        np = (self.position[0]-1, self.position[1])
        if self.map.is_road(np):
            self.position = np

    def move_down(self):
        np = (self.position[0]+1, self.position[1])
        if self.map.is_road(np):
            self.position = np

    def move_left(self):
        np = (self.position[0], self.position[1]-1)
        if self.map.is_road(np):
            self.position = np

    def move_right(self):
        np = (self.position[0], self.position[1]+1)
        if self.map.is_road(np):
            self.position = np

    def face_up(self):
        self.face = Info.FACE_UP
    
    def face_down(self):
        self.face = Info.FACE_DONW
    
    def face_left(self):
        self.face = Info.FACE_LEFT
    
    def face_right(self):
        self.face = Info.FACE_RIGHT

    def get_dict(self):
        return {
            'facing':self.face,
            'vision':self.vision,
            'listen':self.listen,
            'cd':self.cd_count,
            'info':self.info.get_dict(),
            'position':self.position,
            'map':self.map.get_view()
        }
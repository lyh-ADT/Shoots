class Info:
    OP_MOVE_UP = 0
    OP_MOVE_DOWN = 1
    OP_MOVE_LEFT = 2
    OP_MOVE_RIGHT = 3
    FACE_UP = 4
    FACE_DONW = 5
    FACE_LEFT = 6
    FACE_RIGHT = 7
    OP_SHOOT = 8
    
    def __init__(self):
        self.sound = []
        self.shooter = []
    
    def get_dict(self):
        return {
            'sound':self.sound,
            'shooter':self.shooter
        }

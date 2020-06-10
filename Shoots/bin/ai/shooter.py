from Shoots.bin.shooter import Shooter
import random

class RandomAIShooter(Shooter):
    """
    a shooter that act random completely
    """
    def action(self):
        options=[
            self.move_up,
            self.move_down,
            self.move_left,
            self.move_right,
            self.face_up,
            self.face_down,
            self.face_left,
            self.face_right,
            self.shoot
        ]
        op = random.randint(0, len(options)-1)
        options[op]()




class CFRShooter(RandomAIShooter):
    """
    a shooter that trained with CFR
    """
    def __init__(self, map):
        from Shoots.bin.ai.train_cfr import Training
        self.training = Training(0)
        self.training.load("200-6-empty-still.params")
        self.history = ""
        return super().__init__(map)

    def action(self):
        options=[
            self.move_up,
            self.move_down,
            self.move_left,
            self.move_right,
            self.face_up,
            self.face_down,
            self.face_left,
            self.face_right,
            self.shoot
        ]
        infoSet = self.genInfoSet(self.training.history_window)
        try:
            strategy = self.training.nodeMap[infoSet].getStrategy(1)
            op = self.decide(strategy)
            options[op]()
            self.history += self.mapAction(op)
        except KeyError:
            print("miss")
            super().action()

    def decide(self, strategy:list):
        return strategy.index(max(strategy))

    def genInfoSet(self, history_window) -> str:
        """
        build infoSet
        path avaliable: up down left right
        facing enemy: 
        """
        infoSet = ""
        map = self.map
        position = self.position

        infoSet += "1" if len(self.info.shooter) > 0 else "0"
    
        np = (position[0]-1, position[1])
        infoSet += "1" if map.is_road(np) else "0"

        np = (position[0]+1, position[1])
        infoSet += "1" if map.is_road(np) else "0"

        
        np = (position[0], position[1]-1)
        infoSet += "1" if map.is_road(np) else "0"

        
        np = (position[0], position[1]+1)
        infoSet += "1" if map.is_road(np) else "0"

        infoSet += self.history[-history_window*2:]
        return infoSet

    def mapAction(self, action):
        from Shoots.bin.info import Info
        return {
            Info.OP_MOVE_UP:"mu",
            Info.OP_MOVE_DOWN:"md",
            Info.OP_MOVE_LEFT:"ml",
            Info.OP_MOVE_RIGHT:"mr",
            Info.FACE_UP:"fu",
            Info.FACE_DONW:"fd",
            Info.FACE_LEFT:"fl",
            Info.FACE_RIGHT:"fr",
            Info.OP_SHOOT:"st"
        }[action]
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
    pass
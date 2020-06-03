from Shoots.bin.shoots import Shoots
from Shoots.bin.info import Info
from Shoots.bin.ai.shooter import RandomAIShooter as AIShooter

class AIShoots(Shoots):
    """
    automatically add two AIShooter
    """
    def __init__(self):
        super().__init__()
        
        self.players.append(AIShooter(self.map))
        self.players.append(AIShooter(self.map))

        self.viewers = []
        self.view = None

    def update_model(self):
        if [i.dead for i in self.players].count(False) == 1:
            raise Exception("Game over")
        for i in self.players:
            i.action()
        super().update_model()
        fullInfo = Info()
        for j in self.players:
            fullInfo.shooter.append({
                'position':j.position,
                'facing':j.face
            })
        for i in self.viewers:
            i.update_info(fullInfo)

    def update_frame(self):
        if self.update_frame_callback:
            self.update_frame_callback()
    
    def add_player(self):
        player = AIShooter(self.map)
        self.viewers.append(player)
        return player
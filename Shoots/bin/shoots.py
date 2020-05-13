from Shoots.bin.map import Map
from Shoots.bin.shooter import Shooter

class Shoots:
    OP_MOVE_UP = 0
    OP_MOVE_DOWN = 1
    OP_MOVE_LEFT = 2
    OP_MOVE_RIGHT = 3

    def __init__(self):
        self.map = Map(5)
        self.players = []
        self.cur_frame = []
        self.update_frame_callback = None

    def update_model(self):
        pass

    def update_frame(self):
        if self.update_frame_callback:
            self.update_frame_callback()

    def process_input(self, player, operation):
        op = {
            0:lambda x: x.move_up(),
            1:lambda x: x.move_down(),
            2:lambda x: x.move_left(),
            3:lambda x: x.move_right()
        }
        if player not in self.players:
            print("not join player operation !!!", player, operation)
            return
        op[operation](player)

    def add_player(self):
        player = Shooter(self.map)
        self.players.append(player)
        return player

    async def play(self):
        import tornado.gen
        while True:
            self.update_model()
            self.update_frame()
            await tornado.gen.sleep(0.1)
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
        m = self.map.get_view()
        id_offset = 3
        for i, p in enumerate(self.players):
            p_id = i + id_offset
            p_pos = p.position
            m[p_pos[0]][p_pos[1]] = p_id
        self.cur_frame = m

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

    def play(self):
        while True:
            self.update_model()
            self.update_frame()
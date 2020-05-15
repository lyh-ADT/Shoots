from Shoots.bin.map import Map
from Shoots.bin.shooter import Shooter
from Shoots.bin.info import Info

class Shoots:
    def __init__(self):
        self.map = Map(5)
        self.players = []
        self.cur_frame = []
        self.update_frame_callback = None

    def update_model(self):
        for i in self.players:
            targets = []
            if i.shooted:
                targets = i.targets()
                i.shooted = False
            i.cd_count = max(0, i.cd_count-1)
            info = Info()
            for j in self.players:
                if i == j:
                    continue
                if j.position in targets:
                    j.dead = True
                    self.players.remove(j)
                    continue
                if i.can_see(j):
                    info.shooter.append({
                        'position':j.position,
                        'facing':j.face
                    })
            i.update_info(info)

    def update_frame(self):
        if self.update_frame_callback:
            self.update_frame_callback()

    def process_input(self, player, operation):
        op = {
            Info.OP_MOVE_UP:lambda x: x.move_up(),
            Info.OP_MOVE_DOWN:lambda x: x.move_down(),
            Info.OP_MOVE_LEFT:lambda x: x.move_left(),
            Info.OP_MOVE_RIGHT:lambda x: x.move_right(),
            Info.FACE_UP:lambda x: x.face_up(),
            Info.FACE_DONW:lambda x: x.face_down(),
            Info.FACE_LEFT:lambda x: x.face_left(),
            Info.FACE_RIGHT:lambda x: x.face_right(),
            Info.OP_SHOOT:lambda x: x.shoot()
        }
        if player not in self.players:
            print("not join player operation !!!", player, operation)
            return
        op[operation](player)

    def add_player(self):
        player = Shooter(self.map)
        self.players.append(player)
        return player
    
    def remove_player(self, player):
        self.players.remove(player)

    async def play(self):
        import tornado.gen
        while True:
            self.update_model()
            self.update_frame()
            await tornado.gen.sleep(0.1)
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.options
import signal
import json
import threading

from Shoots.bin.ai.shoots import AIShoots, AIShooter
from Shoots.bin.ai.train_cfr import Training, Node

class Server:
    game = AIShoots()
    sockets = []

    class WebSocketHandler(tornado.websocket.WebSocketHandler):
        def open(self):
            self.set_nodelay(True)
            self.shooter = Server.game.add_player()
            Server.sockets.append(self)
            self.send_infomation()

        def on_message(self, message):
            print("this instance not support input")

        def on_close(self):
            Server.sockets.remove(self)
            Server.game.remove_player(self.shooter)
        
        def send_infomation(self):
            self.write_message(self.shooter.get_dict())

    class IndexHandler(tornado.web.RequestHandler):
        def get(self):
            with open("Shoots/bin/ai/server/index.html", 'rb') as f:
                self.write(f.read())

    class Application(tornado.web.Application):
        is_closing = False
        
        def signal_handler(self, signum, frame):
            self.is_closing = True

        def try_exit(self):
            if self.is_closing:
                tornado.ioloop.IOLoop.instance().stop()

    def __init__(self):
        Server.game = AIShoots()
        Server.game.update_frame_callback = self.update_callback
        
    def update_callback(self):
        for i in self.sockets:
            try:
                i.send_infomation()
            except tornado.websocket.WebSocketClosedError:
                Server.game.remove_player(i.shooter)
                self.sockets.remove(i)
        

    def run(self, port):
        application = Server.Application([
            (r"/", Server.IndexHandler),
            (r"/websocket", Server.WebSocketHandler)
        ])
        application.listen(port)
        print("server running...", "port:", port)

        tornado.options.parse_command_line()
        signal.signal(signal.SIGINT, application.signal_handler)
        tornado.ioloop.PeriodicCallback(application.try_exit, 100).start()
        tornado.ioloop.IOLoop.instance().spawn_callback(Server.game.play)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    PORT = 9999
    s = Server()
    s.run(PORT)

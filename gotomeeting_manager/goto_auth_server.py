from werkzeug.serving import make_server
import threading
import flask


class AuthServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 8000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print('Starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


def start_server():
    global server
    app = flask.Flask('myapp')
    server = AuthServerThread(app)
    server.start()
    print('server started')

def stop_server():
    global server
    server.shutdown()
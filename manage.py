from flask import Flask
from flask import render_template
from flask.ext.script import Manager

from mease import Mease
from mease.backends.redis import RedisBackend

mease = Mease(RedisBackend, {})

app = Flask(__name__)
manager = Manager(app)


# -- MEASE

@mease.opener
def websocket_open(client, clients_list):
    client.send("WELCOME")


@mease.receiver
def websocket_message(client, message, clients_list):
    print(message)
    client.send("ECHO")


@mease.sender(routing='flask.test')
def websocket_sender(client, clients_list, message):
    for client in clients_list:
        client.send(message)


# -- COMMANDS

@manager.command
def run_websocket_server():
    mease.run_websocket_server(9090, True)


# -- ROUTES

@app.route("/")
def hello():
    mease.publish('flask.test', message="HELLO WORLD !")
    return render_template('hello.html')


if __name__ == "__main__":
    manager.run()

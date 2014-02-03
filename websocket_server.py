from mease import Mease
from mease.backends.redis import RedisBackend

mease = Mease(RedisBackend, {})


@mease.opener
def websocket_open(client, clients_list):
    client.send("WELCOME")


@mease.receiver
def websocket_message(client, clients_list, message):
    print(message)
    client.send("ECHO")


@mease.sender(routing='flask.test')
def websocket_sender(client, clients_list, message):
    for client in clients_list:
        client.send(message)


if __name__ == '__main__':
    mease.run_websocket_server(port=9090)

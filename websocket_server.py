import logging
import logging.config
from mease import Mease
from mease.backends.redis import RedisBackend

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': '[%(asctime)s] [%(levelname)s] %(log_color)s%(message)s',
            'log_colors': {
                'DEBUG': 'bold_blue',
                'INFO': 'bold_yellow',
                'WARNING': 'bold_orange',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red'
            }
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'mease.websocket_server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': 0
        },
    },
}

logging.config.dictConfig(LOGGING)

mease = Mease(RedisBackend, {})


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


if __name__ == '__main__':
    mease.run_websocket_server(9090, True)

from flask import Flask
from flask import render_template

from mease import Mease
from mease.backends.redis import RedisBackend

app = Flask(__name__)
mease = Mease(RedisBackend, {})


@app.route("/")
def hello():
    mease.publish('flask.test', message="HELLO WORLD !")
    return render_template('hello.html')


if __name__ == '__main__':
    app.run()

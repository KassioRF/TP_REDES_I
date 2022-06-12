from flask import Flask, request
from flask_socketio import SocketIO, emit

from flask import render_template
import pprint

app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*")


clients = []


@app.route("/index")
def index():
    # return "<p>Hello, World!</p>"
    return render_template("index.html")


@app.route("/")
def chat():
    return render_template("chat.html")


# @TODO adicionar o nome do cliente na lista
@io.on("connect")
def onConnect():
    uId = request.sid
    ip = request.remote_addr
    port = request.environ.get("REMOTE_PORT")

    clients.append({"sId": uId, "ip": f"{ip}:{port}"})

    print(pprint.pformat(clients))


@io.on("sendMessage")
def send_handler(msg):
    print(msg)


if __name__ == "__main__":
    io.run(app, debug=True, host="0.0.0.0", port=8000)


"""

1) Enviar uma msg privada pra cada cliente
2) Listar clientes na interface
3) enviar msgs únicas p cada cliente
4) Fazer menu de entrada no lobby*

5) ajustar layout e templates



"""

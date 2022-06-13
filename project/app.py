from flask import Flask, request, redirect, url_for
from flask_socketio import SocketIO, send, emit

from flask import render_template
import time
import pprint


app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*")


clients = {}


@app.route("/")
def index():
    return render_template("enter.html")


@app.route("/<username>")
def chat(username):
    if username not in clients.keys():
        # Garante que só sejam redirecionados para página de msg quem está na lista de clientes
        return redirect(url_for("index"))

    # update sId

    room_clients = list(clients.keys())
    room_clients.remove(username)

    return render_template("chat.html", username=username, clients=room_clients)


# @TODO adicionar o nome do cliente na lista
@io.on("connect")
def connect():
    print(f"\n ---- conected ----\n")


@io.on("username", namespace="/enter")
def enter(username):
    if username not in clients.keys():
        clients[username] = request.sid
        # redirect(url_for("chat", username=username))
        print(f"\n\t --- EMIT ---\n\t")
        io.emit(
            "enter",
            {"url": url_for("chat", username=username)},
            namespace="/enter",
            room=clients[username],
        )

        time.sleep(1)
        io.emit(
            "update",
            {"clients": list(clients.keys())},
            namespace="/lobby",
            broadcast=True,
        )

    else:
        print(f"\n\t --- EMIT FAIL ---\n\t")
        io.emit(
            "enter_error",
            "O Nome já está sendo usado, tente outro",
            namespace="/enter",
            room=request.sid,
        )

    print(clients)


# @TODO Disconnect

# @TODO private messages

if __name__ == "__main__":
    io.run(app, debug=True, host="0.0.0.0", port=8000)


"""

1) Enviar uma msg privada pra cada cliente
2) Listar clientes na interface ok!
4) Fazer menu de entrada no lobby* ok !

5) ajustar layout e templates



"""

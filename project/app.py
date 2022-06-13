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
    # return "<p>Hello, World!</p>"
    print("\n\t - index")
    print(clients)
    print("\n\t - --")
    return render_template("enter.html")


@app.route("/<username>")
def chat(username):
    if username not in clients.keys():
        # Garante que só sejam redirecionados para página de msg quem está na lista de clientes
        return redirect(url_for("index"))

    return render_template("chat.html", clients=clients)


# @app.route("/")
# def chat():
#     return render_template("enter.html")


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
            "enter", {"url": url_for("chat", username=username)}, namespace="/enter"
        )

        # time.sleep(1)

        io.emit("update", {"clients": clients}, namespace="/lobby")

    else:
        print(f"\n\t --- EMIT FAIL ---\n\t")
        io.emit(
            "enter_error", "O Nome já está sendo usado, tente outro", namespace="/enter"
        )

    print(clients)


if __name__ == "__main__":
    io.run(app, debug=True, host="0.0.0.0", port=8000)


"""

1) Enviar uma msg privada pra cada cliente
2) Listar clientes na interface
3) enviar msgs únicas p cada cliente
4) Fazer menu de entrada no lobby*

5) ajustar layout e templates



"""

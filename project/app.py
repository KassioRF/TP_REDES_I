from flask import Flask, request, redirect, url_for
from flask_socketio import SocketIO, send, emit, join_room, leave_room

from flask import render_template
import time
import pprint


app = Flask(__name__)
io = SocketIO(app, cors_allowed_origins="*")


clients = {}


def get_clientIp(request):
    return f"{request.environ['REMOTE_ADDR']}:{request.environ['REMOTE_PORT']}"


# página inicial
@app.route("/")
def index():
    return render_template("enter.html")


# página do chat (lobby/sala)
@app.route("/<username>")
def chat(username):
    if username not in clients.keys():
        # Garante que só sejam redirecionados para página de msg quem está na lista de clientes
        return redirect(url_for("index"))

    # define a lista de clientes conectados no lobby
    room_clients = clients.copy()
    room_clients.pop(username)

    return render_template("chat.html", username=username, clients=room_clients)


# Atualiza a porta do cliente que entrou no lobby
@io.on("connect_lobby", namespace="/lobby")
def connect(username):
    leave_room(clients[username])

    room = get_clientIp(request)
    join_room(room)
    clients[username] = room

    io.emit(
        "client_room",
        {"ip": clients[username]},
        namespace="/lobby",
        room=clients[username],
    )

    # Atualiza os clientes com a nova lista de pessoas conectadas no lobby
    print(f"\n\t --- Atualiza a lista de clientes para todos no lobby ---\n")
    io.emit(
        "update",
        {"clients": clients},
        namespace="/lobby",
        broadcast=True,
    )


# Remove o cliente desconectado da lista de clientes ativos
@io.on("disconnect", namespace="/lobby")
def disconnect():
    key = [k for k, v in clients.items() if v == get_clientIp(request)][0]
    clients.pop(key)

    # Atualiza os clientes com a nova lista de pessoas conectadas no lobby
    if clients:
        io.emit(
            "update",
            {"clients": clients, "disconected": key},
            namespace="/lobby",
            broadcast=True,
        )


# Envia o ip local do usuário quando ele está na página de registro
@io.on("connect", namespace="/enter")
def return_ip():
    room = get_clientIp(request)
    join_room(room)
    # retorna o ip do cliente que será informado na tela de registro
    io.emit("ip", {"ip": request.environ["REMOTE_ADDR"]}, namespace="/enter", room=room)


# Registra um novo cliente no servidor
@io.on("username", namespace="/enter")
def enter(username):
    if username not in clients.keys():
        clients[username] = get_clientIp(request)
        # Redireciona o cliente para a página do lobby
        io.emit(
            "enter",
            {"url": url_for("chat", username=username)},
            namespace="/enter",
            room=get_clientIp(request),
        )

    else:
        # Caso o nome seja inválido, retorna um feedback para o usuário
        print(f"\n\t --- EMIT FAIL ---\n\t")
        io.emit(
            "enter_error",
            "O Nome já está sendo usado, tente outro",
            namespace="/enter",
            room=get_clientIp(request),
        )


# Trata o envio de mensagens
@io.on("send_message", namespace="/lobby")
def send_message(data):
    # obtem o usuario de origem
    username = [k for k, v in clients.items() if v == get_clientIp(request)][0]

    # envia a msg para o usuario de destino
    emit(
        "new_message",
        {"client": username, "msg": data["message"], "date": data["date"]},
        room=clients[data["client"]],
    )


if __name__ == "__main__":
    io.run(app, debug=False, host="0.0.0.0", port=1997)

from flask import Flask, request, redirect, url_for
from flask_socketio import SocketIO, send, emit

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
    print(f"\n\t ---- {get_clientIp(request)} ---- \n")
    return render_template("enter.html")


# página do lobby
@app.route("/<username>")
def chat(username):
    if username not in clients.keys():
        # Garante que só sejam redirecionados para página de msg quem está na lista de clientes
        return redirect(url_for("index"))

    # define a lista de clientes conectados no lobby
    room_clients = list(clients.keys())
    room_clients.remove(username)

    return render_template("chat.html", username=username, clients=room_clients)


# Atualiza a porta do cliente que entrou no lobby
@io.on("connect_lobby", namespace="/lobby")
def connect(username):
    clients[username] = request.sid


# Remove o cliente desconectado da lista de clientes ativos
@io.on("disconnect", namespace="/lobby")
def disconnect():
    key = [k for k, v in clients.items() if v == request.sid][0]
    clients.pop(key)

    # Atualiza os clientes com a nova lista de pessoas conectadas no lobby
    if clients:
        io.emit(
            "update",
            {"clients": list(clients.keys()), "disconected": key},
            namespace="/lobby",
            broadcast=True,
        )


# Registra um novo cliente no servidor
@io.on("username", namespace="/enter")
def enter(username):
    if username not in clients.keys():
        clients[username] = request.sid
        # Redireciona o cliente para a página do lobby
        io.emit(
            "enter",
            {"url": url_for("chat", username=username)},
            namespace="/enter",
            room=request.sid,
        )

        # Atualiza os clientes com a nova lista de pessoas conectadas no lobby
        print(f"\n\t --- update via broad cast client list on lobby---\n\t")
        io.emit(
            "update",
            {"clients": list(clients.keys())},
            namespace="/lobby",
            broadcast=True,
        )

    else:
        # Caso o nome seja inválido, retorna um feedback para o usuário
        print(f"\n\t --- EMIT FAIL ---\n\t")
        io.emit(
            "enter_error",
            "O Nome já está sendo usado, tente outro",
            namespace="/enter",
            room=request.sid,
        )


# Trata o envio de mensagens
@io.on("send_message", namespace="/lobby")
def send_message(data):
    # obtem o usuario de origem
    username = [k for k, v in clients.items() if v == request.sid][0]

    # envia a msg para o usuario de destino
    emit(
        "new_message",
        {"client": username, "msg": data["message"], "date": data["date"]},
        room=clients[data["client"]],
    )


if __name__ == "__main__":
    io.run(app, debug=False, host="0.0.0.0", port=1997)


"""

1) Enviar uma msg privada pra cada cliente
2) Listar clientes na interface ok!
4) Fazer menu de entrada no lobby* ok !

5) ajustar layout e templates
================================

# Resolver notificações chat
# Adicionar IP e porta no login 
# utilizar IP e porta no lugar do request.sid


"""

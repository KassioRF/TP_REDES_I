
var chat_area = document.getElementById('chat-area');
var open_chats = {};
var clients_control = clients ? clients : {};


/** Adiciona evento de click nos clientes carregados no inicio da sessão*/
$('.user-list').on('click', e => {
  open_chat_window(e.target.id);

  //limpa as notificações de novas msgs
  let el = $(`#${e.target.id}`).children('.notify-dot');
  el.attr('data-notify', '');
  el.html('');

});

/** Atualiza a lista a interface com clientes conectados */
function update_lobby(clients_, username) {
  clients_control = clients_;

  let clients = Object.keys(clients_);
  $("#user-list-el").html("");
  clients.forEach(c => {
    if (c != username) {
      $("#user-list-el").append(`<span id="${c}" class="user-list"><span class="user-icon far fa-dot-circle"></span> ${c} <span class="notify-dot badge bg-danger rounded-pill" data-notify=""></span> </span> `);
    }
  });
  /*--- Atualiza os eventos de click para os clientes listados na sessão ---*/
  $('.user-list').on('click', e => {
    open_chat_window(e.target.id);

    //limpa as notificações de novas msgs
    let el = $(`#${e.target.id}`).children('.notify-dot');
    el.attr('data-notify', '');
    el.html('');

  });
}

/**Remove clientes que desconectaram */
function remove_client(client) {
  if (open_chats[client]) {
    delete open_chats[client];
  }

  if (el = document.querySelector(`[data=${client}]`)) {
    alert(`${client} saiu da sala`);
    chat_area.innerHTML = '';
  }
}


/** abre janela de chat */
function open_chat_window(client) {
  el = document.querySelector(`[data=${client}]`);
  if (!el) {
    // cria uma nova janela
    chat_area.innerHTML = '';

    chat_window = open_chats[client] ? open_chats[client] : build_chat_view(client);

    open_chats[client] = chat_window;

    chat_area.append(chat_window);

    //adiciona evento de enviar p / client
    document.getElementById(`send;${client}`).addEventListener('click', e => {
      send_message(client);
    });

  }

}

/** cria uma nova janela */
function build_chat_view(client) {
  let window_ = document.createElement('div');
  let header = document.createElement('div');
  let body = document.createElement('div');
  let sender = document.createElement('div');

  window_.className = 'chat-window';
  window_.setAttribute('data', `${client}`);

  header.className = 'chat-header';
  header.innerHTML = `<h5> ${client} </h5> <span class="text-muted"> ${clients_control[client]}</span>`;

  body.className = 'chat-body';

  sender.className = 'chat-sender';
  sender.innerHTML = (
    '<div class="input-group">' +
    `<button id=send;${client} class="input-group-text"><span class="fas fa-paper-plane"></span></button>` +
    `<textarea class="form-control" data-send=${client}></textarea>` +
    '</div></div>'
  );

  window_.appendChild(header);
  window_.appendChild(body);
  window_.appendChild(sender);

  return window_;

}


function append_msg(client, msg, date, type) {
  //verifica se já existe um chat aberto, caso contrário é necessário criar o elemento
  if (!open_chats[client]) {
    open_chats[client] = build_chat_view(client);
  }

  let msgEl = create_msg_element(msg, date, type);

  open_chats[client].querySelector('.chat-body').append(msgEl);


  //notify
  el = document.querySelectorAll(`[data=${client}]`);

  if (el.length == 0) {
    notify_new_msg(client);
  }


}


function notify_new_msg(client) {
  let el = $(`#${client}`).children('.notify-dot');
  let qtd = el.attr('data-notify');

  if (qtd == '') {
    qtd = 1;
  } else {
    qtd = parseInt(qtd) + 1;
  }

  el.attr('data-notify', qtd);
  el.html(qtd);

}

function create_msg_element(msg_, date_, type) {
  let msgType = type == 'send' ? 'your-msg' : 'client-msg';

  let div = document.createElement('div');
  let msg = document.createElement('p');
  let date = document.createElement('p');

  div.className = 'chat-msg ' + msgType;
  msg.innerHTML = msg_;

  date.className = "text-muted msg-hour";
  date.innerHTML = date_;

  div.append(msg);
  div.append(date);

  return div;

}

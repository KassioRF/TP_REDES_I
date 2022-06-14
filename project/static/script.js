
var chat_area = document.getElementById('chat-area');
var open_chats = [];
console.log(chat_area);
/** Adiciona evento de click nos clientes carregados no inicio da sessão*/
$('.user-list').on('click', e => {
  open_chat_window(e.target.id);
});

/** Atualiza a lista a interface com clientes conectados */
function update_lobby(clients, username) {
  $("#user-list-el").html("");
  clients.forEach(c => {
    if (c != username) {
      $("#user-list-el").append(`<span id="${c}" class="user-list"><span class="user-icon far fa-dot-circle"></span> ${c} </span>`);
    }
  });
  /*--- Atualiza os eventos de click para os clientes listados na sessão ---*/
  $('.user-list').on('click', e => {
    open_chat_window(e.target.id);
  });

}


/** abre janela de chat */
function open_chat_window(client) {
  el = document.querySelectorAll(`[data=${client}]`);
  if (el.length == 0) {
    // cria uma nova janela
    chat_area.innerHTML = '';
    chat_area.append(build_chat_view(client));

    //adiciona evento de enviar p/ client
    document.getElementById(`send;${client}`).addEventListener('click', e => {
      //@TODO pegar msg e chamar evento de envio!
    });

  } else {
    // abre a janela existente
    console.log('retorna o chat existente')
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
  header.innerHTML = `<h5> ${client} </h5>`;

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

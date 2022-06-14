
/** Atualiza a lista a interface com clientes conectados */
function update_lobby(clients, username) {
  $("#user-list-el").html("");
  clients.forEach(c => {
    if (c != username) {
      $("#user-list-el").append(`<span class="user-list"><span class="user-icon far fa-dot-circle"></span> ${c} </span>`);
    }
  });
}



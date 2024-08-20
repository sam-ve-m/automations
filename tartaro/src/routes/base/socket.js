const representation_name = document.getElementById("query").textContent;
const resource_name = window.location.pathname.split("/")[1];
const page = resource_name + "/" + representation_name;
var sub_representation = "";
var active_highlights = {};
var highlights = {};
var details = "";

function connect_to_socket(url, on_message_function) {
  web_socket = new WebSocket(url);
  web_socket.onmessage = on_message_function;
  web_socket.reconnect = function() {
        var new_websocket = connect_to_socket(url, on_message_function);
        new_websocket.onclose = this.onclose;
        return new_websocket;
  };
  return web_socket
}

var message_socket = connect_to_socket('ws://localhost:3334/ws/message/' + page, function(event) {
    const figure_as_html = event.data;
    const graphs = document.getElementById("graphs");
    graphs.innerHTML = figure_as_html;
    Array.from(graphs.querySelectorAll("script")).forEach( oldScript => {
        const newScript = document.createElement("script");
        Array.from(oldScript.attributes).forEach( attr => newScript.setAttribute(attr.name, attr.value) );
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode.replaceChild(newScript, oldScript);
    });
    event.preventDefault();
});
message_socket.onclose = function(e) {
        message_socket = message_socket.reconnect();
};
function request_reset(){
    message_socket.send("{}");
    active_highlights = {};
    highlights = {};
}
function request_filter(highlights){
    message_socket.send(JSON.stringify(highlights));
};

var details_socket = connect_to_socket('ws://localhost:3334/ws/details/' + resource_name, function(event) {
    const ticker_details = event.data;
    const ticker_details_placeholder = document.getElementById("ticker_details_placeholder");
    ticker_details_placeholder.innerHTML = ticker_details;
    Array.from(ticker_details_placeholder.querySelectorAll("script")).forEach( oldScript => {
        const newScript = document.createElement("script");
        Array.from(oldScript.attributes).forEach( attr => newScript.setAttribute(attr.name, attr.value) );
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode.replaceChild(newScript, oldScript);
    });
});
details_socket.onclose = function(e) {
        details_socket = details_socket.reconnect();
};
function request_details(ticker){
    details_socket.send(ticker);
};


var update_socket = connect_to_socket('ws://localhost:3334/ws/update', function(event) {
    notification = event.data;
    window.alert(notification);
});
update_socket.onclose = function(e) {
        update_socket = update_socket.reconnect();
};
function request_update(ticker_fields){
    const password = prompt("Você tem certeza que deseja atualizar o banco de dados? Digite a senha: ");
    if (password != null){
        const payload = {'ticker_fields': ticker_fields, 'password': password};
        update_socket.send(JSON.stringify(payload));
    };
};

function download_excel(excel_file_as_bytes, file_name){
    var link = document.createElement('a');
    link.href = window.URL.createObjectURL(excel_file_as_bytes);
    link.download=file_name + ".xls";
    link.click();
    const excel_buttons = document.getElementsByClassName("excel_button");
    for (var button_div of excel_buttons){
        var button = button_div.getElementsByTagName("button")[0];
        button.disabled = false;
    };
}

var excel_socket = connect_to_socket('ws://localhost:3334/ws/excel/' + page, function(event) {
    var file_name = representation_name + "__";
    if (sub_representation != representation_name){
        file_name += sub_representation + "__";
    }
    Object.getOwnPropertyNames(highlights).forEach(coll =>
        Object.getOwnPropertyNames(highlights[coll]).forEach(field =>
            file_name += field + ":" + String(highlights[coll][field]) + "-"
        )
    );
    var excel_file_as_bytes = event.data;
    download_excel(excel_file_as_bytes, file_name);
});
excel_socket.onclose = function(e) {
        excel_socket = excel_socket.reconnect();
};
function request_excel(resource, representation){
    sub_representation = representation;
    const payload = {'representation': representation, 'highlights': highlights};
    excel_socket.send(JSON.stringify(payload));
};


var excel_details_socket = connect_to_socket('ws://localhost:3334/ws/excel/details', function(event) {
    var excel_file_as_bytes = event.data;
    download_excel(excel_file_as_bytes, details);
});
excel_details_socket.onclose = function(e) {
        excel_details_socket = excel_details_socket.reconnect();
};
function request_details_excel(){
    excel_details_socket.send(details);
};



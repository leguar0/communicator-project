"use strict";


if(USER_ID == null || USER_ID == -1)
    window.open("login.html","_self");
const currentUserNamePlaceholderElement = document.querySelector("#current-user-name");
if(currentUserNamePlaceholderElement != null && USER_FULLNAME != null)
    currentUserNamePlaceholderElement.innerText = ` ${USER_FULLNAME}`;

const userId = USER_ID;
const searchParams = new URLSearchParams(location.search.substring(1));
const receiverId = searchParams.get("id");
const receiverFullname = searchParams.get("fullname");

if(receiverFullname != null)
    document.querySelector("#receiver-fullname").innerText = receiverFullname;

async function get_msgs(){
    let url = `http://localhost:8000/get_messages?cur_user=${userId}&from_user=${receiverId}`;
    let response = await fetch(url);
    if(response.ok){
        let resp_data = await response.json();

        for(let i =0;i<resp_data.length;++i){
            let from = resp_data[i][2];
            displayMessage(from, resp_data[i][0]);
        }

    }
}
get_msgs();

const websocket = new WebSocket(`ws://localhost:8000/ws/${userId}`);

websocket.onopen = function(event) {
    console.log("WebSocket connection established.");
};

websocket.onmessage = function(event) {
    const m = JSON.parse(event.data);
    if(m.id_sender != receiverId) return;
    displayMessage(m.id_sender, m.message);
};

websocket.onclose = function(event) {
    console.log("WebSocket connection closed.");
};

function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const message = messageInput.value.trim();
    if (message !== "") {

        let data = {
            id_sender: userId,
            id_receiver: parseInt(receiverId),
            message: message
        };

        websocket.send(JSON.stringify(data));
        messageInput.value = "";
        displayMessage(userId, message);
    }
}

function displayMessage(senderId, msg) {
    const chatMessages = document.getElementById("chat-messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("msg-holder");
    messageElement.classList.add(userId == senderId ? "msg-to" : "msg-from");
    messageElement.textContent = msg;
    chatMessages.appendChild(messageElement);
}
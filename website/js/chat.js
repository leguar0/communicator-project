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

const messageInput = document.querySelector("#message-input");

async function get_msgs(){
    let url = `http://localhost:8000/get_messages?cur_user=${userId}&from_user=${receiverId}`;
    let response = await fetch(url);
    if(response.ok){
        let data = await response.json();

        for(let i=0;i<data.length;++i)
            displayMessage(data[i]["id_sender"], data[i]["message"]);

    }
}
get_msgs();

const websocket = new WebSocket(`ws://localhost:8000/ws/${userId}/${receiverId}`);

websocket.onopen = function(event) {
    console.log("WebSocket connection established.");
};

websocket.onmessage = function(event) {
    const m = JSON.parse(event.data);
    displayMessage(m.id_sender, m.message);
};

websocket.onclose = function(event) {
    console.log("WebSocket connection closed.");
};

function sendMessage() {
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
    messageElement.innerHTML = emojione.toImage(msg);;
    chatMessages.appendChild(messageElement);
}

document.querySelector("#send-btn").addEventListener("click",()=>{
    sendMessage();
});

messageInput.addEventListener("keypress", (e)=>{
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

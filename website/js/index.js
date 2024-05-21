"use strict";

if(USER_ID == null || USER_ID == -1)
    window.open("login.html","_self");
const currentUserNamePlaceholderElement = document.querySelector("#current-user-name");
if(currentUserNamePlaceholderElement != null && USER_FULLNAME != null)
    currentUserNamePlaceholderElement.innerText = ` ${USER_FULLNAME}`;

const usersHolder = document.querySelector("#online-users-holder");
async function get_current_users(){
    let url = `http://localhost:8000/current_users`;
    let response = await fetch(url);
    if(response.ok){
        let resp_data = await response.json();
        console.log(resp_data)

        for(let i =0;i<resp_data.length;++i){

            if(resp_data[i].id == USER_ID)
                continue;

            let a = document.createElement("a");
            a.href=`chat.html?id=${resp_data[i].id}&fullname=${resp_data[i].name} ${resp_data[i].surname}`;
            a.id = "user_id_" + resp_data[i].id;

            let div_container = document.createElement("div");
            div_container.classList.add("user-holder");
            
            let div_name = document.createElement("div");
            div_name.innerHTML = `${resp_data[i].name} ${resp_data[i].surname}#${resp_data[i].id}`;
            div_container.appendChild(div_name);

            let div_msg_count = document.createElement("div");
            div_msg_count.classList.add("msg-count");
            div_container.appendChild(div_msg_count);

            a.appendChild(div_container);
            
            usersHolder.appendChild(a);

            count_unread_messages(resp_data[i].id)
        }
    }
}

async function count_unread_messages(is_sender){
    let url = `http://localhost:8000/count_unread_messages_from_user?id_sender=${is_sender}&id_receiver=${USER_ID}`
    let response = await fetch(url);
    if(response.ok){
        let resp_data = await response.json();
        if(resp_data == 0) return;
        document.querySelector(`#user_id_${is_sender} .msg-count`).innerHTML += `📩${resp_data}`;
    }
}

get_current_users();
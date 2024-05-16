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

            let div = document.createElement("div");
            div.innerHTML = `${resp_data[i].name} ${resp_data[i].surname}`;
            div.classList.add("user-holder");
            
            a.appendChild(div)
            
            usersHolder.appendChild(a);
        }
    }
}
get_current_users();
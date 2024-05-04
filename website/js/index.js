"use strict";

const userId = sessionStorage.getItem("user_id");

const usersHolder = document.querySelector("#online-users-holder");
async function get_current_users(){
    let url = `http://localhost:8000/current_users`;
    let response = await fetch(url);
    if(response.ok){
        let resp_data = await response.json();
        console.log(resp_data)

        for(let i =0;i<resp_data.length;++i){

            if(resp_data[i].id == userId)
                continue;

            let a = document.createElement("a");
            a.href="chat.html?"+ resp_data[i].id;
            a.id = "user_id_" + resp_data[i].id;

            let div = document.createElement("div");
            div.innerHTML = resp_data[i].name;
            div.classList.add("user-holder");
            
            a.appendChild(div)
            
            usersHolder.appendChild(a);
        }
    }
}
get_current_users();
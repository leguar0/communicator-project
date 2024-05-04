"use strict";

const usernameInput = document.querySelector("#login-input");
const passwordInput = document.querySelector("#password-input");

document.querySelector("#login-btn").addEventListener("click",()=>{

    if(usernameInput.value == "" || passwordInput.value =="") return;

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/login");
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const body = JSON.stringify({
        id: -1,
        username: usernameInput.value,
        password: passwordInput.value
    });
    xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
        let user = JSON.parse(xhr.responseText);

        sessionStorage.setItem("user_id", user.id );
        if(user.id != -1)
            window.open("index.html","_self");

    } else {
        console.log(`Error: ${xhr.status}`);
    }
    };
    xhr.send(body);
});
"use strict";

const usernameInput = document.querySelector("#login-input");
const passwordInput = document.querySelector("#password-input");
const loginStatus = document.querySelector("#login-status");
const loginBtn = document.querySelector("#login-btn");

loginBtn.addEventListener("click",()=>{

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
            if(user.id == -1){
                loginStatus.innerHTML = "Nie udało się zalogować";
                return;
            }

            login(user.id, user.name, user.surname);
            if(sessionStorage.getItem("user_id") != null)
                window.open("index.html","_self");
            else
                loginStatus.innerHTML = "Nie udało się zalogować";

        } else {
            console.log(`Error: ${xhr.status}`);
        }
    };
    xhr.send(body);
});

usernameInput.addEventListener("focus", ()=>{
    loginStatus.innerHTML = "";
});

passwordInput.addEventListener("focus", ()=>{
    loginStatus.innerHTML = "";
});

usernameInput.addEventListener("keypress", (e)=>{
    if (e.key === "Enter") {
      e.preventDefault();
      loginBtn.click();
    }
});

passwordInput.addEventListener("keypress", (e)=>{
    if (e.key === "Enter") {
      e.preventDefault();
      loginBtn.click();
    }
});

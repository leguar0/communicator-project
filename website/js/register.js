"use strict";

const nameInput = document.querySelector("#name-input");
const surnameInput = document.querySelector("#surname-input");
const usernameInput = document.querySelector("#username-input");
const passwordInput = document.querySelector("#password-input");

const registerStatus = document.querySelector("#register-status");


document.querySelector("#register-btn").addEventListener("click",()=>{

    if(nameInput.value == "" || surnameInput.value == "" || usernameInput.value == "" || passwordInput.value == "")
        return;
    
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:8000/register_user");
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    const body = JSON.stringify({
        id: -1,
        name: nameInput.value,
        surname: surnameInput.value,
        username: usernameInput.value,
        password: passwordInput.value
    });
    xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
        let user = JSON.parse(xhr.responseText);
        if(user.id == -1)
            registerStatus.innerHTML = "Nie udało się zarejestrować";
        else
            window.open("login.html","_self");
    } else {
        console.log(`Error: ${xhr.status}`);
    }
    };
    xhr.send(body);
});

nameInput.addEventListener("focus", ()=>{
    registerStatus.innerHTML = "";
});

surnameInput.addEventListener("focus", ()=>{
    registerStatus.innerHTML = "";
});

usernameInput.addEventListener("focus", ()=>{
    registerStatus.innerHTML = "";
});

passwordInput.addEventListener("focus", ()=>{
    registerStatus.innerHTML = "";
});
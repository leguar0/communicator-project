"use strict";

const nameInput = document.querySelector("#name-input");
const surnameInput = document.querySelector("#surname-input");
const usernameInput = document.querySelector("#username-input");
const passwordInput = document.querySelector("#password-input");

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
    if (xhr.readyState == 4 && xhr.status == 201) {
        console.log(JSON.parse(xhr.responseText));
    } else {
        console.log(`Error: ${xhr.status}`);
    }
    };
    xhr.send(body);
});
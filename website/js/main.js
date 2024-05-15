"use strict";

const USER_ID = sessionStorage.getItem("user_id");
const USER_FULLNAME = sessionStorage.getItem("user_fullname");

function login(userId, userName, userSurname){
    sessionStorage.setItem("user_id", userId);
    sessionStorage.setItem("user_fullname", `${userName} ${userSurname}`);
}

function logout(){
    sessionStorage.removeItem("user_id");
    sessionStorage.removeItem("user_fullname");
}
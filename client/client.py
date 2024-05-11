from email import message
import requests
import importlib
from collections import UserList
import dis
import datetime
import time
import websocket
import json
from threading import *
import tkinter as tk
from tkinter import messagebox
from gui.login import LoginInterface
from gui.register import RegisterInterface
from gui.menu import MenuInterface
from gui.chat import ChatInterface

class Client:
    def __init__(self):
        self.cur_user_id = -1
        self.login_interface = None
        self.menu_interface = None
        self.register_interface = None
        self.chat_interface = None
    
    def set_login_interface(self, login_interface):
        self.login_interface = login_interface

    def login_button(self, username, password):
        try:
            user_json = {"id": 0, "username": username, "password": password}
            result = requests.post('http://127.0.0.1:8000/login', json=user_json)
        
            if result.status_code == 200:
                res = result.json()
                if res["id"] != -1:
                    self.cur_user_id = res["id"]
                    self.login_interface.close_window()
                    self.menu_interface = MenuInterface(self)
                    self.menu_interface.create_window()
                else:
                    self.login_interface.show_messagebox("ERROR", "Sprawdz login i haslo")    
        except Exception as e:
            print(e)
            
    def get_users(self):
        response = requests.get('http://127.0.0.1:8000/current_users')
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def send_message(self, message, other_user_id):  
        cur_user_id = self.cur_user_id
        id_receiver = other_user_id
        if id_receiver != 0:
            message_json = {"id_sender": cur_user_id, "id_receiver": id_receiver, "message": message}
            requests.post('http://127.0.0.1:8000/send_message', json=message_json)
            message_json = {
                "message": message,
                "id_sender": cur_user_id
            }
            self.chat_interface.show_message(self.chat_inerface.scrollable_frame, cur_user_id, message_json)
            
    def register_user(self, name, surname, username, password):
        user_json = {"id": 0, "name": name, "surname": surname,"username": username, "password": password}
        result = requests.post('http://127.0.0.1:8000/register_user', json=user_json)
        if result.status_code == 200:
            cur_user_id = result.json()["id"]
            messagebox.showinfo("Sukces", f"Uzytkownik zarejestrowany pomyslnie. ID: {cur_user_id}")
        
            reg.destroy()  
            login.login_window() 
        else:
            messagebox.showerror("Blad", "Nie udalo sie zarejestrowac uzytkownika.")

    def get_unread_messages_count(self, user_id):
        response = requests.get(f'http://127.0.0.1:8000/count_unread_messages_from_user?id_sender={user_id}&id_receiver={self.cur_user_id}')
        if response.status_code == 200:
            return response.json()
        else:
            return 0
        
    def get_messages(self, user_id):
        response = requests.get(f"http://localhost:8000/get_messages?cur_user={self.cur_user_id}&from_user={user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return [] 

if __name__ == "__main__":
    client = Client()
    login_interface = LoginInterface(client.login_button)
    client.set_login_interface(login_interface)
    login_interface.run()
from email import message
import requests
import importlib
from collections import UserList
import dis
import datetime
import time
import websocket
import json
import threading
import tkinter as tk
from tkinter import messagebox
from gui.login import LoginInterface
from gui.register import RegisterInterface
from gui.menu import MenuInterface
from gui.chat import ChatInterface

adress_ip = "127.0.0.1"

class Client:
    def __init__(self):
        self.cur_user_id = -1
        self.user = None
        self.other_user_id = -1
        self.login_interface = None
        self.menu_interface = None
        self.register_interface = None
        self.chat_interface = None
    
    def set_interfaces(self, login_interface):
        self.login_interface = login_interface
        
    def login_button(self, username, password):
        try:
            user_json = {"id": 0, "username": username, "password": password}
            result = requests.post(f'http://{adress_ip}:8000/login', json=user_json)
        
            if result.status_code == 200:
                res = result.json()
                print(res)
                if res["id"] != -1:
                    self.cur_user_id = res["id"]
                    self.user = res
                    self.login_interface.close_window()
                    self.menu_interface = MenuInterface(self)
                    self.menu_interface.create_window()
                else:
                    self.login_interface.show_messagebox("Blad", "Sprawdz login i haslo")    
        except Exception as e:
            print(e)
            
    def login_rg_button(self):
        self.login_interface.close_window()
        self.register_interface = RegisterInterface(self)
        self.register_interface.create_window()
       
    def back_login(self):
        self.register_interface.close_window()
        self.login_interface.create_window()
        
    def back_menu(self):
        self.chat_interface.close_window()
        self.ws.close()
        self.menu_interface.create_window()

    def register_button(self, name, surname, username, password):
        try:
            user_json = {"id": 0, "name": name, "surname": surname,"username": username, "password": password}
            result = requests.post(f'http://{adress_ip}:8000/register_user', json=user_json)
            if result.status_code == 200:
                res = result.json()
                if res["id"] != - 1:
                    self.register_interface.show_messagebox("Sukces", "Udalo sie zarejestrowac uzytkownika")
                    self.register_interface.close_window()
                    self.back_login()
                else:
                    self.register_interface.show_messagebox("Blad", "Uzupelnij poprawnie wszystkie pola")
            else:
                self.register_interface.show_messagebox("Blad", "Nie udalo sie zarejestrowac uzytkownika.")
        except Exception as e:
            print(e)
            
    def chat_button(self, other_user_id):
        self.other_user_id = other_user_id

        if self.other_user_id != -1:
            self.menu_interface.close_window()

            self.chat_interface = ChatInterface(self)
            self.chat_interface.create_window()

            self.threading(self.chat_interface.get_scrollable_frame(), self.get_cur_user_id()) 
            self.chat_interface.run()

    def logout(self):
        self.cur_user_id = -1
        self.menu_interface.close_window()
        self.login_interface.create_window()

    def get_other_user_id(self):
        return self.other_user_id

    def get_cur_user_id(self):
        return self.cur_user_id

    def get_name_surname(self):
        users = self.get_users()
        
        for user in users:
            if user["id"] == self.other_user_id:
                _name_surname = user["name"] + " " + user["surname"]
                return _name_surname

    def get_user(self):
        return self.user

    def get_users(self):
        response = requests.get(f'http://{adress_ip}:8000/current_users')
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def send_message(self, message):  
        cur_user_id = self.cur_user_id
        id_receiver = self.other_user_id
        if id_receiver != 0:
            message_json = {"id_sender": cur_user_id, "id_receiver": id_receiver, "message": message}
            requests.post(f'http://{adress_ip}:8000/send_message', json=message_json)
            message_json = {
                "message": message,
                "id_sender": cur_user_id
            }           

    def get_unread_messages_count(self, user_id):
        response = requests.get(f'http://{adress_ip}:8000/count_unread_messages_from_user?id_sender={user_id}&id_receiver={self.cur_user_id}')
        if response.status_code == 200:
            return response.json()
        else:
            return 0
        
    def get_messages(self):
        if self.other_user_id != -1:    
            response = requests.get(f"http://{adress_ip}:8000/get_messages?cur_user={self.cur_user_id}&from_user={self.other_user_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return [] 

    def threading(self, scrollable_frame, cur_user_id): 
        t1=threading.Thread(target=self.work, args=[scrollable_frame, cur_user_id]) 
        t1.start() 
      
    def work(self, scrollable_frame, cur_user_id): 
        def on_message(ws, message):
            try:
                message_json = json.loads(message)
                self.chat_interface.show_message(scrollable_frame, message_json["message"], message_json["id_sender"])
                print(f"Received message: {message}")
            except json.JSONDecodeError as e:
                pass

        def on_error(ws, error):
            print(f"Error: {error}")

        def on_close(ws, status, message):
            print("### Closed ###")

        def on_open(ws):
            print("### OPEN ###")

        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(f"ws://{adress_ip}:8000/ws/{cur_user_id}",
                                        on_message = on_message,
                                        on_error = on_error,
                                        on_close = on_close)
        self.ws.on_open = on_open
        self.ws.run_forever()

            
if __name__ == "__main__":
    client = Client()
    login_interface = LoginInterface(client)
    client.set_interfaces(login_interface)
    login_interface.run()
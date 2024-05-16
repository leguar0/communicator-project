from collections import UserList
import dis
from re import S
import tkinter as tk
from tkinter import messagebox
import requests
import datetime

class MenuInterface:
    def __init__(self, client):
        self.client = client
       
    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Komunikator")

        _width = 800
        _height = 600
    
        _screen_width = self.root.winfo_screenwidth()
        _screen_height = self.root.winfo_screenheight()
    
        _posx = (_screen_width - _width) // 2
        _posy = (_screen_height - _height) // 2

        self.root.geometry(f"{_width}x{_height}+{_posx}+{_posy}")

        self.refresh_button = tk.Button(self.root, text="Odswiez", command=self.refresh, bg="#e6a565", bd=1)
        self.refresh_button.grid(row=0, column=0, padx=10, pady=5)
        
        self.logout_button = tk.Button(self.root, text="Wyloguj", command=self.logout, bg="#e6a565", bd=1)
        self.logout_button.grid(row=0, column=1, padx=10, pady=5)

        self.users_frame = tk.Frame(self.root)
        self.users_frame.grid(row=1, column=0)
        
        self.display_users()

    def display_users(self):
        users_label = tk.Label(self.users_frame, text="Lista uzytkownikow:")
        users_label.grid(row=0, column=0, padx=5, pady=5)
        _users_list = self.client.get_users()
        i = 0
        for user in _users_list:
            user_id = user["id"]
            if user_id != self.client.cur_user_id:
                surname = user["surname"]
                unread_messages_count = self.client.get_unread_messages_count(user_id)
                user_label_text = f"{surname} ({unread_messages_count} nieprzeczytane)"
                user_button = tk.Button(self.users_frame, text=user_label_text, command=lambda uid=user_id: self.open_chat(uid))
                user_button.grid(row=i + 1, column=0, padx=5, pady=5, sticky="nsew")
                i += 1

    def refresh(self):
        for widget in self.users_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        self.display_users()
        
    def logout(self):
        self.client.logout()
        
    def open_chat(self, other_user_id):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.client.chat_button(other_user_id)
        
    def close_window(self):
        self.root.destroy()
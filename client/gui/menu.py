from collections import UserList
import dis
from re import S
import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar,messagebox
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

        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.grid(row=0, column=0)

        _user = self.client.get_user()
        name_label = tk.Label(self.button_frame, text=f'Imie: {_user["name"]}\n Nazwisko: {_user["surname"]}')
        name_label.grid(row = 1, column=1)

        self.refresh_button = tk.Button(self.button_frame, text="Odswiez", command=self.refresh, bg="#e6a565", bd=1)
        self.refresh_button.grid(row=0, column=2, padx=10, pady=5)
        
        self.logout_button = tk.Button(self.button_frame, text="Wyloguj", command=self.logout, bg="#e6a565", bd=1)
        self.logout_button.grid(row=0, column=1, padx=10, pady=5)

        self.users_frame = ttk.Frame(self.root)
        
        self.canvas = tk.Canvas(self.users_frame)
        self.scrollbar = ttk.Scrollbar(self.users_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.users_frame.grid(row=1, column=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


        self.display_users()

    def display_users(self):
        users_label = tk.Label(self.scrollable_frame, text="Lista uzytkownikow:")
        users_label.grid(row=0, column=0, padx=5, pady=5)
        _users_list = self.client.get_users()
        i = 0
        for user in _users_list:
            user_id = user["id"]
            if user_id != self.client.cur_user_id:
                surname = user["surname"]
                unread_messages_count = self.client.get_unread_messages_count(user_id)
                user_label_text = f"{surname} ({unread_messages_count} nieprzeczytane)"
                user_button = tk.Button(self.scrollable_frame, text=user_label_text, command=lambda uid=user_id: self.open_chat(uid))
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
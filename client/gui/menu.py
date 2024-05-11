from collections import UserList
import dis
from re import S
import tkinter as tk
from tkinter import messagebox
import requests
import datetime

class MenuInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Komunikator")
        self.create_window()
        self.display_users()

    def create_window(self):
        _width = 800
        _height = 600
    
        _screen_width = self.root.winfo_screenwidth()
        _screen_height = self.root.winfo_screenheight()
    
        _posx = (_screen_width - _width) // 2
        _posy = (_screen_height - _height) // 2

        self.root.geometry(f"{_width}x{_height}+{_posx}+{_posy}")
    
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
    
        self.users_frame = tk.Frame(self.root)
        self.users_frame.pack()
            
        inbox_button = tk.Button(self.button_frame, text="Skrzynka pocztowa", command=lambda: open_inbox_window(cur_user_id), width=10, bg="red")
        inbox_button.grid(row=0, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")
      
        inbox_button = tk.Button(self.button_frame, text="Odswiez", command=lambda: refresh(button_frame_users, cur_user_id), width=10, bg="red")
        inbox_button.grid(row=0, column=1, columnspan=2, padx=10, pady=5,sticky="nsew")
    
    def run(self):
        self.root.mainloop()

    def display_users(self, cur_user_id, users_list):
        users_label = tk.Label(self.users_frame, text="Lista uzytkownikow:")
        users_label.grid(row=2, column=0, padx=5, pady=5)
        for user in users_list:
            user_id = user["id"]
            surname = user["surname"]
            unread_messages_count = users_list[user["id"]]
            user_label_text = f"{surname} ({unread_messages_count} nieprzeczytane)"
            user_button = tk.Button(self.users_frame, text=user_label_text, command=lambda user_id=user_id: open_chat_window(window, cur_user_id, user_id))
            user_button.grid(row=3 + user_id, column=0, padx=5, pady=5, sticky="nsew")

    def refresh(self, cur_user_id, users_list):
        for widget in self.users_frame.winfo_children():
            if isinstance(widget,tk.Button):
                widget.destroy()
        self.display_users(cur_user_id, users_list)

    def open_inbox_window(window,cur_user_id):
   
        window.destroy()  
        inbox.inbox_window(cur_user_id)  
    
    def open_chat_window(window,cur_user_id,user_id):
   
        window.destroy() 
        chat.chat_window(cur_user_id,user_id)  
    

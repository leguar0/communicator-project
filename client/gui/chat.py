from re import S
import tkinter as tk
from tkinter import Scrollbar, messagebox
from turtle import left, right
from unittest import result
from tkinter import ttk

class ChatInterface:
    def __init__(self, client):
        self.client = client

    def create_window(self):
        self.root = tk.Tk()
        self.root.title(f'Chat: {self.client.get_name_surname()}')
    
        chat_frame_main = ttk.Frame(self.root,height=450,width=400 )    
        canvas = tk.Canvas(chat_frame_main)
        scrollbar = ttk.Scrollbar(chat_frame_main, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        
        chat_frame_main.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        chat_frame_second = tk.Frame(self.root)
        chat_frame_second.pack()
    

        _width = 800
        _height = 600
    
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
    
        _posx = (screen_width - _width) // 2
        _posy = (screen_height - _height) // 2

    
        self.root.geometry(f"{_width}x{_height}+{_posx}+{_posy}")
    
        chat_frame_second.pack()

        message_label = tk.Label(chat_frame_second, text="Tresc wiadomosci:")
        message_label.pack(padx=5, pady=5, anchor="w")

        self.message_entry = tk.Entry(chat_frame_second)
        self.message_entry.pack(padx=5, pady=5, fill="x")

        return_button = tk.Button(chat_frame_second, text="Powrot", command=self.client.back_menu, width=10, bg="#e6a565", bd=1)
        return_button.pack(padx=10, pady=5, fill="x")

        send_message_button = tk.Button(chat_frame_second, text="Wyslij wiadomosc", command=self.send_message, state="active", bg="#e6a565", bd=1)
        send_message_button.pack(padx=5, pady=5, fill="x")
        
        self.show_messages()

    def show_messages(self):
        messages = self.client.get_messages()  
        for message in messages:
            self.show_message(message["message"], message["id_sender"])
   
    def show_message(self, message, _id):
        message_frame = tk.Label(self.scrollable_frame, text=message, width=25, wraplength=100)
        if _id == self.client.get_other_user_id():
            message_frame.config(bg="green")
            message_frame.grid(column=0)
        else:
            message_frame.config(bg="yellow")
            message_frame.grid(column=1)
            
    def send_message(self):
        _message = self.message_entry.get()
        
        self.show_message(_message, self.client.get_cur_user_id())
        self.client.send_message(_message)
            
    def close_window(self):
        self.root.destroy()
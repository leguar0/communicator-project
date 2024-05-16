from re import S
import tkinter as tk
from tkinter import Scrollbar, messagebox
from turtle import left, right
from unittest import result
import requests
import websocket
import json
from tkinter import ttk
from threading import *

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

        message_entry = tk.Entry(chat_frame_second)
        message_entry.pack(padx=5, pady=5, fill="x")

        return_button = tk.Button(chat_frame_second, text="Powrot", command=self.client.back_menu, width=10,height=2,bg="red")
        return_button.pack(padx=10, pady=5, fill="x")

        send_message_button = tk.Button(chat_frame_second, text="Wyslij wiadomosc", command=lambda: send_message(message_entry,other_user_id,cur_user_id,scrollable_frame), state="active")
        send_message_button.pack(padx=5, pady=5, fill="x")
         
        def threading(cur_user_id): 
            t1=Thread(target=work, args=[cur_user_id]) 
            t1.start() 
  
        def work(cur_user_id): 
  
            def on_message(ws, message):
                try:
                    message_json = json.loads(message)
                    self.show_message(message_json)
                    print(f"Received message: {message}")
                except json.JSONDecodeError as e:
                    pass

            def on_error(ws, error):
                print(f"Error: {error}")

            def on_close(ws):
                print("### Closed ###")

            def on_open(ws):
                print("### OPEN ###")

            websocket.enableTrace(True)
            ws = websocket.WebSocketApp(f"ws://localhost:8000/ws/{cur_user_id}",
                                        on_message = on_message,
                                        on_error = on_error,
                                        on_close = on_close)
            ws.on_open = on_open
            ws.run_forever()

        threading(self.client.get_cur_user_id())
    
    def show_messages(self, cur_user_id,user_id):
        messages = self.client.get_messages(cur_user_id,user_id)  
        for message in messages:
            self.show_message(message)
   
    def show_message(self, message):
        print(message)
        message_frame = tk.Label(self.scrollable_frame, text=message["message"],width=25, wraplength=100)
        if message["id_sender"] == self.client.get_other_user_id:
            message_frame.config(bg="green")
            message_frame.grid(column=1)
        else:
            message_frame.config(bg="yellow")
            message_frame.grid(column=0)
            
    def close_window(self):
        self.root.destroy()

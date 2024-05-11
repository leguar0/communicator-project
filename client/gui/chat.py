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
    pass

    def open_menu_menu(chat,cur_user_id):
   
        chat.destroy() 
        menu.window_window(cur_user_id)


    def show_messages(scrollable_frame,cur_user_id,user_id):
        messages = get_messages(cur_user_id,user_id)  
        print(messages)
        for message in messages:
            show_message(scrollable_frame, cur_user_id, message)
   
    def show_message(scrollable_frame,cur_user_id, message):
        print(message)
        message_frame = tk.Label(scrollable_frame, text=message["message"],width=25, wraplength=100)
        if message["id_sender"] == cur_user_id:
            message_frame.config(bg="green")
            message_frame.grid(column=1)
        else:
            message_frame.config(bg="yellow")
            message_frame.grid(column=0)

    def chat_window(cur_user_id,other_user_id):
    
        chat = tk.Tk()
        chat.title("chat")
    
        chat_frame_main = ttk.Frame(chat,height=450,width=400 )    
        canvas = tk.Canvas(chat_frame_main)
        scrollbar = ttk.Scrollbar(chat_frame_main, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        show_messages(scrollable_frame, cur_user_id, other_user_id)

        chat_frame_main.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        chat_frame_second = tk.Frame(chat)
        chat_frame_second.pack()
    

        menu_width = 800
        menu_height = 600
    
        screen_width = chat.winfo_screenwidth()
        screen_height = chat.winfo_screenheight()
    
        x_position = (screen_width - menu_width) // 2
        y_position = (screen_height - menu_height) // 2

    
        chat.geometry(f"{menu_width}x{menu_height}+{x_position}+{y_position}")
    
        chat_frame_second.pack()

        message_label = tk.Label(chat_frame_second, text="Tresc wiadomosci:")
        message_label.pack(padx=5, pady=5, anchor="w")

        message_entry = tk.Entry(chat_frame_second)
        message_entry.pack(padx=5, pady=5, fill="x")

        return_button = tk.Button(chat_frame_second, text="Powrot", command=lambda: open_menu_menu(chat,cur_user_id), width=10,height=2,bg="red")
        return_button.pack(padx=10, pady=5, fill="x")

        send_message_button = tk.Button(chat_frame_second, text="Wyslij wiadomosc", command=lambda: send_message(message_entry,other_user_id,cur_user_id,scrollable_frame), state="active")
        send_message_button.pack(padx=5, pady=5, fill="x")
         
        def threading(cur_user_id, scrollable_frame): 
            t1=Thread(target=work, args=[cur_user_id, scrollable_frame]) 
            t1.start() 
  
        def work(cur_user_id, scrollable_frame): 
  
            def on_message(ws, message):
                try:
                    message_json = json.loads(message)
                    print(message_json)
                    show_message(scrollable_frame, cur_user_id, message_json)
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

        threading(cur_user_id, scrollable_frame)
    
    def run():
        self.chat.mainloop()

if __name__ == "__main__":
    chat_menu()
    

def get_messages(cur_user_id,user_id):
    url = f"http://localhost:8000/get_messages?cur_user={cur_user_id}&from_user={user_id}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return [] 
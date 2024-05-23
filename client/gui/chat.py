from asyncio.windows_events import NULL
from re import S
import tkinter as tk
from tkinter import Scrollbar, messagebox
from turtle import left, right
from unittest import result
from tkinter import ttk
import emoji

class ChatInterface:
    def __init__(self, client):
        self.client = client

    def create_window(self):
        self.root = tk.Tk()
        self.root.title(f'Chat: {self.client.get_name_surname()}')
    
        chat_frame_main = ttk.Frame(self.root,height=550,width=750)    
        self.canvas = tk.Canvas(chat_frame_main,height=450,width=450)
        self.scrollbar = ttk.Scrollbar(chat_frame_main, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        chat_frame_main.pack()
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

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
        
        self.message_entry = tk.Entry(chat_frame_second, width=50)
        self.message_entry.pack(padx=5, pady=5, fill="x", expand=True)

        self.message_entry.bind("<Return>", self.send_message_with_event)

        send_message_button = tk.Button(chat_frame_second, text="Wyslij wiadomosc", command=self.send_message, bg="#e6a565", bd=1)
        send_message_button.pack(padx=5, pady=5, fill="x")
        
        return_button = tk.Button(chat_frame_second, text="Powrot", command=self.client.back_menu, bg="#e6a565", bd=1)
        return_button.pack(padx=5, pady=5, fill="x")

        self.root.protocol("WM_DELETE_WINDOW", self.client.back_menu)
        
        self.show_messages()

    def get_scrollable_frame(self):
        return self.scrollable_frame

    def show_messages(self):
        messages = self.client.get_messages()  
        for message in messages:
            self.show_message(self.scrollable_frame, message["message"], message["id_sender"])
   
    def show_message(self, scrollable_frame, message, _id):
        message = emoji.emojize(message, language='alias')
        message_frame = tk.Label(scrollable_frame, text=message, width=25, wraplength=200, font=("Arial", 12))
        if _id == self.client.get_other_user_id():
            message_frame.config(bg="green")
            message_frame.grid(column=0)
        else:
            message_frame.config(bg="yellow")
            message_frame.grid(column=1)
        self.root.update_idletasks()
        self.scroll_to_bottom()
            
    def send_message(self):
        _message = self.message_entry.get()
        self.message_entry.delete('0', 'end')

        self.show_message(self.scrollable_frame, _message, self.client.get_cur_user_id())
        self.client.send_message(_message)
        
    def scroll_to_bottom(self):
        self.root.update_idletasks() 
        self.root.after(100, self.scrollbar.set, 2, 2)
        self.root.after(100, self.canvas.yview_moveto, 1)

    def send_message_with_event(self, event):
        self.send_message()

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()
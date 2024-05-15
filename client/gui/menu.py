from collections import UserList
import dis
import tkinter as tk
from tkinter import messagebox
import requests
import inbox
import chat
import datetime

def display_users(window,Button_frame_users, cur_user_id, users_list):
    users_label = tk.Label(Button_frame_users, text="Lista uzytkownikow:")
    users_label.grid(row=2, column=0, padx=5, pady=5)
    for user in users_list:
        user_id = user["id"]
        if user_id == cur_user_id:
            continue
        surname = user["surname"]
        unread_messages_count = get_unread_messages_count(cur_user_id, user_id)
        user_label_text = f"{surname} ({unread_messages_count} nieprzeczytane)"
        user_button = tk.Button(Button_frame_users, text=user_label_text, command=lambda user_id=user_id: open_chat_window(window, cur_user_id, user_id))
        user_button.grid(row=3 + user_id, column=0, padx=5, pady=5, sticky="nsew")

def open_inbox_window(window,cur_user_id):
   
    window.destroy()  
    inbox.inbox_window(cur_user_id)  
    
def open_chat_window(window,cur_user_id,user_id):
   
    window.destroy() 
    chat.chat_window(cur_user_id,user_id)  
    

    

def window_window(cur_user_id):
    

    window = tk.Tk()
    window.title("window")
    
    button_frame_main = tk.Frame(window)
    button_frame_main.pack()
    
    button_frame_users = tk.Frame(window)
    button_frame_users.pack()
    

    def refresh(window,button_frame_users, cur_user_id):
        for widget in button_frame_users.winfo_children():
            if isinstance(widget,tk.Button):
                widget.destroy()
        users_list = get_current_users()
        
        display_users(window,button_frame_users, cur_user_id, users_list)

    window_width = 800
    window_height = 600
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    inbox_button = tk.Button(button_frame_main, text="Skrzynka pocztowa", command=lambda: open_inbox_window(window, cur_user_id), width=10, height=2, bg="red")
    inbox_button.grid(row=0, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")

      
    inbox_button = tk.Button(button_frame_main, text="Odswiez", command=lambda: refresh(window,button_frame_users, cur_user_id), width=10, height=2, bg="red")
    inbox_button.grid(row=0, column=1, columnspan=2, padx=10, pady=5,sticky="nsew")
    


    refresh(window,button_frame_users, cur_user_id)
    
  
    window.mainloop()
    

def get_current_users():
    url = "http://localhost:8000/current_users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []  

def get_unread_messages_count(cur_user_id, user_id):
    url = f'http://127.0.0.1:8000/count_unread_messages_from_user?id_sender={user_id}&id_receiver={cur_user_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 0

if __name__ == "__main__":
    window_window()
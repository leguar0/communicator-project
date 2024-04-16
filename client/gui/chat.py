import tkinter as tk
from tkinter import messagebox
from unittest import result
import requests
import menu
import register

def start_chat():
    # Tu umie�� kod do rozpocz�cia czatu
    pass

def open_menu_window(chat,cur_user_id):
   
    chat.destroy()  # Zniszczenie okna rejestracji
    menu.menu_window(cur_user_id)  # Otwarcie okna logowania

def send_message(message_entry,other_user_id,cur_user_id):  


    message = message_entry.get()
    id_receiver = other_user_id
    if id_receiver != 0:
        url = f'http://127.0.0.1:8000/send_message'
        requests.post(url, json={"id_sender": cur_user_id, "id_receiver": id_receiver, "message": message})
        messagebox.showinfo("Sukces", "Wiadomosc wyslana pomyslnie.")
    else:
        messagebox.showerror("Blad", "Zle ID odbiorcy.")
        

def chat_window(cur_user_id,other_user_id):
    
    chat = tk.Tk()
    chat.title("Chat")
    
    print(cur_user_id)
    print(other_user_id)
    

    window_width = 800
    window_height = 600
    
    screen_width = chat.winfo_screenwidth()
    screen_height = chat.winfo_screenheight()
    
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    chat.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    message_label = tk.Label(chat, text="Tresc wiadomosci:")
    message_label.grid(row=0, column=0, padx=5, pady=5,sticky="nsew")
    message_entry = tk.Entry(chat)
    message_entry.grid(row=0, column=1, padx=5, pady=5,sticky="nsew")
    
    return_button = tk.Button(chat, text="Powrot", command=lambda: open_menu_window(chat,cur_user_id), width=10,height=2,bg="red")
    return_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")
    
    send_message_button = tk.Button(chat, text="Wyslij wiadomosc", command=lambda: send_message(message_entry,other_user_id,cur_user_id), state="active")
    send_message_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5,sticky="nsew")
    

    chat.mainloop()

if __name__ == "__main__":
    chat_window()
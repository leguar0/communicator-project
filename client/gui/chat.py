import tkinter as tk
from tkinter import messagebox
from unittest import result
import requests
import menu
import register

def start_chat():
    # Tu umieœæ kod do rozpoczêcia czatu
    pass

def open_menu_window(chat):
   
    chat.destroy()  # Zniszczenie okna rejestracji
    menu.menu_window()  # Otwarcie okna logowania

def send_message(message_entry,id_receiver_entry):  


    message = message_entry.get()
    id_receiver = id_receiver_entry.get()
    cur_user_id = register.result.json()["id"] 
    if id_receiver != 0:
        url = f'http://127.0.0.1:8000/send_message'
        requests.post(url, json={"id_sender": cur_user_id, "id_receiver": id_receiver, "message": message})
        messagebox.showinfo("Sukces", "Wiadomosc wyslana pomyslnie.")
    else:
        messagebox.showerror("Blad", "Zle ID odbiorcy.")
        

def chat_window():
    
    chat = tk.Tk()
    chat.title("Chat")
    

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

    id_receiver_label = tk.Label(chat, text="Do uzytkownika o ID:")
    id_receiver_label.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
    id_receiver_entry = tk.Entry(chat)
    id_receiver_entry.grid(row=1, column=1, padx=5, pady=5,sticky="nsew")
    
    return_button = tk.Button(chat, text="Powrot", command=lambda: open_menu_window(chat), width=10,height=2,bg="red")
    return_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")
    
    send_message_button = tk.Button(chat, text="Wyslij wiadomosc", command=lambda: send_message(message_entry,id_receiver_entry), state="active")
    send_message_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5,sticky="nsew")
    
    print(register.result.json()["id"])

    chat.mainloop()

if __name__ == "__main__":
    chat_window()
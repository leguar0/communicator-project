import tkinter as tk
from tkinter import messagebox
import requests
import time

def register_user():
    global result 
    name = name_entry.get()
    surname = surname_entry.get()
    
    user_json = {"id": 0, "name": name, "surname": surname}
    url = 'http://127.0.0.1:8000/register_user'
    result = requests.post(url, json=user_json)
    
    if result.status_code == 200:
        cur_user_id = result.json()["id"]
        messagebox.showinfo("Sukces", f"Uzytkownik zarejestrowany pomyslnie. ID: {cur_user_id}")
        send_message_button.config(state="normal")
        unread_messages_button.config(state="normal")
    else:
        messagebox.showerror("Blad", "Nie udalo sie zarejestrowac uzytkownika.")

def send_message():
    message = message_entry.get()
    id_receiver = id_receiver_entry.get()
    cur_user_id = result.json()["id"] 
    if id_receiver != 0:
        url = f'http://127.0.0.1:8000/send_message'
        requests.post(url, json={"id_sender": cur_user_id, "id_receiver": id_receiver, "message": message})
        messagebox.showinfo("Sukces", "Wiadomosc wyslana pomyslnie.")
    else:
        messagebox.showerror("Blad", "Zle ID odbiorcy.")

def check_unread_messages():
    cur_user_id = result.json()["id"] 
    url = f'http://127.0.0.1:8000/unread_messages?id_user={cur_user_id}'
    unread_messages = requests.get(url).json()
    if len(unread_messages) > 0:
        messagebox.showinfo("Nieprzeczytane wiadomosci", f"Masz {len(unread_messages)} nieprzeczytanych wiadomosci")

root = tk.Tk()
root.title("Komunikator")

window_width = 800
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

name_label = tk.Label(root, text="Imie:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

surname_label = tk.Label(root, text="Nazwisko:")
surname_label.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
surname_entry = tk.Entry(root)
surname_entry.grid(row=1, column=1, padx=5, pady=5,sticky="nsew")

register_button = tk.Button(root, text="Zarejestruj", command=register_user, width=10,height=2,bg="red")
register_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5,sticky="nsew")

message_label = tk.Label(root, text="Tresc wiadomosci:")
message_label.grid(row=3, column=0, padx=5, pady=5,sticky="nsew")
message_entry = tk.Entry(root)
message_entry.grid(row=3, column=1, padx=5, pady=5,sticky="nsew")

id_receiver_label = tk.Label(root, text="Do uzytkownika o ID:")
id_receiver_label.grid(row=4, column=0, padx=5, pady=5,sticky="nsew")
id_receiver_entry = tk.Entry(root)
id_receiver_entry.grid(row=4, column=1, padx=5, pady=5,sticky="nsew")

send_message_button = tk.Button(root, text="Wyslij wiadomosc", command=send_message, state="disabled")
send_message_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5,sticky="nsew")

unread_messages_button = tk.Button(root, text="Sprawdz nieprzeczytane wiadomosci", command=check_unread_messages, state="disabled")
unread_messages_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5,sticky="nsew")

root.mainloop()

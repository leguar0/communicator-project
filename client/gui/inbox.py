import tkinter as tk
from tkinter import messagebox
import requests
import menu
import register
import login

def display_inbox():
    pass

def open_menu_menu(inbox):
   
    inbox.destroy()  
    menu.window_window(cur_user_id)  
 
def check_unread_messages(cur_user_id):

    print(cur_user_id)
    url = f'http://127.0.0.1:8000/unread_messages?id_user={cur_user_id}'
    unread_messages = requests.get(url).json()
    if len(unread_messages) > 0:
        messagebox.showinfo("Nieprzeczytane wiadomosci", f"Masz {len(unread_messages)} nieprzeczytanych wiadomosci")
    
def inbox_menu(cur_user_id):
     
    inbox = tk.Tk()
    inbox.title("Inbox")
    

    menu_width = 800
    menu_height = 600
    
    screen_width = inbox.winfo_screenwidth()
    screen_height = inbox.winfo_screenheight()
    
    x_position = (screen_width - menu_width) // 2
    y_position = (screen_height - menu_height) // 2

    inbox.geometry(f"{menu_width}x{menu_height}+{x_position}+{y_position}")
    
    name_label = tk.Label(inbox, text="Imie:")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(inbox)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    surname_label = tk.Label(inbox, text="Nazwisko:")
    surname_label.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
    surname_entry = tk.Entry(inbox)
    surname_entry.grid(row=1, column=1, padx=5, pady=5,sticky="nsew")
    
    return_button = tk.Button(inbox, text="Powrot", command=lambda: open_menu_menu(inbox), width=10,height=2,bg="red")
    return_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")
    
    unread_messages_button = tk.Button(inbox, text="Sprawdz nieprzeczytane wiadomosci", command=lambda: check_unread_messages(cur_user_id), state="active")
    unread_messages_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5,sticky="nsew")



    inbox.mainloop()

if __name__ == "__main__":
    inbox_menu(cur_user_id)
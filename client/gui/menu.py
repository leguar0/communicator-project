import tkinter as tk
from tkinter import messagebox
import requests
import inbox
import chat

def display_menu():
    # Tu umieœæ kod menu wyboru u¿ytkownika i opcji
    pass

def open_inbox_window(menu,cur_user_id):
   
    menu.destroy()  # Zniszczenie okna rejestracji
    inbox.inbox_window(cur_user_id)  # Otwarcie okna logowania
    
def open_chat_window(menu,cur_user_id,user_id):
   
    menu.destroy()  # Zniszczenie okna rejestracji
    chat.chat_window(cur_user_id,user_id)  # Otwarcie okna logowania
    

def display_menu(users_list):
    # Tu umieœæ kod menu wyboru u¿ytkownika i opcji
    pass

def menu_window(cur_user_id):
    
    users_list = get_current_users()
        
    menu = tk.Tk()
    menu.title("Menu")
    

    window_width = 800
    window_height = 600
    
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    menu.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    inbox_button = tk.Button(menu, text="Skrzynka pocztowa", command=lambda: open_inbox_window(menu, cur_user_id), width=10, height=2, bg="red")
    inbox_button.grid(row=0, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")

    users_label = tk.Label(menu, text="Lista uzytkownikow:")
    users_label.grid(row=2, column=0, padx=5, pady=5)


    # Wype³nij listê u¿ytkowników
    for user in users_list:
        user_id = user["id"]
        username = user["username"]
        # Pobierz liczbê nieprzeczytanych wiadomoœci od danego u¿ytkownika
        unread_messages_count = get_unread_messages_count(cur_user_id, user_id)
        # Twórz etykietê z nazw¹ u¿ytkownika i liczb¹ nieprzeczytanych wiadomoœci
        user_label_text = f"{username} ({unread_messages_count} nieprzeczytane)"
        user_button = tk.Button(menu, text=user_label_text, command=lambda user_id=user_id: open_chat_window(menu, cur_user_id, user_id))
        user_button.grid(row=3 + user_id, column=0, padx=5, pady=5, sticky="nsew")

    menu.mainloop()
    

def get_current_users():
    url = "http://localhost:8000/current_users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []  

def get_unread_messages_count(cur_user_id, user_id):
    url = 'http://127.0.0.1:8000/count_unread_messages_from_user?id_sender={user_id}&id_receiver={cur_user_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 0

if __name__ == "__main__":
    menu_window("current_user_id")
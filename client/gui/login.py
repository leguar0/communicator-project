import tkinter as tk
from tkinter import messagebox
from unittest import result
import requests
import importlib
import register
import menu
import inbox



def login(username_entry, password_entry, log):
    username = username_entry.get()
    password = password_entry.get()

    url = f'http://127.0.0.1:8000/login?username={username}&password={password}'

    try:
        response = requests.get(url)
        res = response.json()

        if response.status_code == 200:
            if len(res) > 0:
                cur_user_id = res["id"]
                inbox.cur_user_id = cur_user_id
                messagebox.showinfo("Sukces", f"Zalogowano pomyslnie. ID uzytkownika: {cur_user_id}")
                log.destroy()
                users = get_users()
                menu.window_window(cur_user_id)
        else:
            messagebox.showerror("Blad", "Blad logowania. Sprawdz login i haslo.")
    except Exception as e:
        print(e)
        pass
    
def get_users():
    url = 'http://127.0.0.1:8000/current_users' 
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def open_register_menu(log):
        log.destroy()
        register.register_menu()

def login_menu():
    
    
    log = tk.Tk()
    log.title("Logowanie")
    

    menu_width = 800
    menu_height = 600
    
    screen_width = log.winfo_screenwidth()
    screen_height = log.winfo_screenheight()
    
    x_position = (screen_width - menu_width) // 2
    y_position = (screen_height - menu_height) // 2

    log.geometry(f"{menu_width}x{menu_height}+{x_position}+{y_position}")
    

    
    username_label = tk.Label(log, text="Nazwa:")
    username_label.grid(row=2, column=0, padx=5, pady=5)
    username_entry = tk.Entry(log)
    username_entry.grid(row=2, column=1, padx=5, pady=5)

    password_label = tk.Label(log, text="Haslo:")
    password_label.grid(row=3, column=0, padx=5, pady=5,sticky="nsew")
    password_entry = tk.Entry(log,show="*")
    password_entry.grid(row=3, column=1, padx=5, pady=5,sticky="nsew")
    

    login_button = tk.Button(log, text="Zaloguj", command=lambda: login(username_entry,password_entry,log), width=10,height=2,bg="red")
    login_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5,sticky="nsew")
    
    register_button = tk.Button(log, text="Zarejestruj", command=lambda: open_register_menu(log))
    register_button.grid(row=5, column=1, padx=5, pady=5,sticky="nsew")
        

    log.mainloop()

if __name__ == "__main__":
    login_menu()
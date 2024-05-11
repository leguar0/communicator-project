import tkinter as tk
from tkinter import messagebox
import requests
import time

class RegisterInterface:
    def __init__(self):
        self.root = tk.Tk()

    def open_login_window(reg):
   
        reg.destroy()  # Zniszczenie okna rejestracji
        login.login_window()  # Otwarcie okna logowania

    def register_window():
    
    
        reg = tk.Tk()
        reg.title("Rejestracja")
    

        window_width = 800
        window_height = 600
    
        screen_width = reg.winfo_screenwidth()
        screen_height = reg.winfo_screenheight()
    
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        reg.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
        name_label = tk.Label(reg, text="Imie:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(reg)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        surname_label = tk.Label(reg, text="Nazwisko:")
        surname_label.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
        surname_entry = tk.Entry(reg)
        surname_entry.grid(row=1, column=1, padx=5, pady=5,sticky="nsew")
    
        username_label = tk.Label(reg, text="Nazwa:")
        username_label.grid(row=2, column=0, padx=5, pady=5)
        username_entry = tk.Entry(reg)
        username_entry.grid(row=2, column=1, padx=5, pady=5)

        password_label = tk.Label(reg, text="Haslo:")
        password_label.grid(row=3, column=0, padx=5, pady=5,sticky="nsew")
        password_entry = tk.Entry(reg)
        password_entry.grid(row=3, column=1, padx=5, pady=5,sticky="nsew")
    

    
        register_button = tk.Button(reg, text="Zarejestruj", command=lambda: register_user(name_entry,surname_entry,username_entry,password_entry,reg), width=10,height=2,bg="blue")
        register_button.grid(row=1, column=2, columnspan=2, padx=10, pady=5,sticky="nsew")
    
        return_button = tk.Button(reg, text="Powrot do logowania", command=lambda: open_login_window(reg))
        return_button.grid(row=5, column=0, columnspan=2, padx=10, pady=2,sticky="nsew")
         
    def run():
        self.root.mainloop()

if __name__ == "__main__":
    register_window()
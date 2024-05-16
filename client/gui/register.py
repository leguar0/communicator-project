import tkinter as tk
from tkinter import messagebox
import time

class RegisterInterface:
    def __init__(self, client):
        self.client = client
        self.root = None

    def create_window(self):
        if self.root is not None:
            self.root.destroy()

        self.root = tk.Tk()
        self.root.title("Rejestracja")

        _width = 800
        _height = 600
    
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
    
        _posx = (screen_width - _width) // 2
        _posy = (screen_height - _height) // 2

        self.root.geometry(f"{_width}x{_height}+{_posx}+{_posy}")
    
        name_label = tk.Label(self.root, text="Imie:")
        name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        surname_label = tk.Label(self.root, text="Nazwisko:")
        surname_label.grid(row=1, column=0, padx=5, pady=5,sticky="nsew")
        self.surname_entry = tk.Entry(self.root)
        self.surname_entry.grid(row=1, column=1, padx=5, pady=5,sticky="nsew")
    
        username_label = tk.Label(self.root, text="Nazwa:")
        username_label.grid(row=2, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)

        password_label = tk.Label(self.root, text="Haslo:")
        password_label.grid(row=3, column=0, padx=5, pady=5,sticky="nsew")
        self.password_entry = tk.Entry(self.root)
        self.password_entry.grid(row=3, column=1, padx=5, pady=5,sticky="nsew")
    
        register_button = tk.Button(self.root, text="Zarejestruj", command=self.button_register_click, bg="#e6a565")
        register_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    
        return_button = tk.Button(self.root, text="Powrot do logowania", command=self.button_back_click, bg="#e6a565")
        return_button.grid(row=6, column=0, columnspan=2, padx=10, pady=2, sticky="nsew")
        
        self.warning_label = tk.Label(self.root, text="Uzupelnij wszystkie pola", fg="red")
        self.warning_label.grid(row=7, column=0, sticky="nsew")  
        self.hide_warning() 
        
    def get_name(self):
        return self.name_entry.get()
    
    def get_surname(self):
        return self.surname_entry.get()
    
    def get_username(self):
        return self.username_entry.get()
    
    def get_password(self):
        return self.password_entry.get()
    
    def show_warning(self):
        self.warning_label.grid(row=7, column=1, sticky="nsew")

    def hide_warning(self):
        self.warning_label.grid_forget()

    def show_messagebox(self, name, text):
        if name == "Sukces":
            messagebox.showinfo(name, text)
        else:
            messagebox.showerror(name, text)
        
    def button_back_click(self):
        self.client.back_login()

    def button_register_click(self):
        _name = self.name_entry.get()
        _surname = self.surname_entry.get()
        _username = self.username_entry.get()
        _password = self.password_entry.get()
        
        if not _name or not _surname or not _username or not _password:
            self.show_warning()
        else:
            self.hide_warning()
            self.client.register_button(_name, _surname, _username, _password)
            
    def close_window(self):
        if self.root:
            self.root.destroy()
            self.root = None
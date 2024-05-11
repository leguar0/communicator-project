import tkinter as tk
from tkinter import messagebox
from turtle import color
from unittest import result

class LoginInterface:
    def __init__(self, button_callback):
         self.root = tk.Tk()
         self.root.title("Logowanie")
         self.button_callback = button_callback
         self.create_window()
         
    def create_window(self):
        _width = 800
        _height = 600

        _screen_width = self.root.winfo_screenwidth()
        _screen_height = self.root.winfo_screenheight()
        
        _posx = (_screen_width - _width) // 2
        _posy = (_screen_height - _height) // 2

        self.root.geometry(f"{_width}x{_height}+{_posx}+{_posy}")
        
        username_label = tk.Label(self.root, text="Nazwa:")
        username_label.grid(row=2, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)

        password_label = tk.Label(self.root, text="Haslo:")
        password_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        login_button = tk.Button(self.root, text="Zaloguj", width=10, command=self.button_click, bg="#e6a565", bd=1)
        login_button.grid(row=5, column=1, sticky="nsew")
        
        register_button = tk.Button(self.root, text="Zarejestruj", width=10, bg="#e6a565", bd=1)
        register_button.grid(row=6, column=1, sticky="nsew")

        self.warning_label = tk.Label(self.root, text="Uzupelnij wszystkie pola", fg="red")
        self.warning_label.grid(row=7, column=1, sticky="nsew")  
        self.hide_warning() 

    def button_click(self):
        _username = self.username_entry.get()
        _password = self.password_entry.get()
        
        if not _username or not _password:
            self.show_warning()
        else:
            self.hide_warning()
            self.button_callback(_username, _password)

    def show_warning(self):
        self.warning_label.grid(row=7, column=1, sticky="nsew")

    def hide_warning(self):
        self.warning_label.grid_forget()
    
    def show_messagebox(self, name, text):
        messagebox.showerror(name, text)

    def get_username(self):
        return self.username_entry.get();

    def get_password(self):
        return self.password_entry.get();

    def close_window(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop() 
        
if __name__ == "__main__":
    login_interface = LoginInterface()
    login_interface.run()
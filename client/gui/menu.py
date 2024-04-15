import tkinter as tk
from tkinter import messagebox
import requests
import inbox
import chat

def display_menu():
    # Tu umieœæ kod menu wyboru u¿ytkownika i opcji
    pass

def open_inbox_window(menu):
   
    menu.destroy()  # Zniszczenie okna rejestracji
    inbox.inbox_window()  # Otwarcie okna logowania
    
def open_chat_window(menu):
   
    menu.destroy()  # Zniszczenie okna rejestracji
    chat.chat_window()  # Otwarcie okna logowania

def menu_window():
    
    # Funkcja tworz¹ca okno glowne
    
    menu = tk.Tk()
    menu.title("Menu")
    

    window_width = 800
    window_height = 600
    
    screen_width = menu.winfo_screenwidth()
    screen_height = menu.winfo_screenheight()
    
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    menu.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    inbox_button = tk.Button(menu, text="Skrzynka pocztowa", command=lambda: open_inbox_window(menu), width=10,height=2,bg="red")
    inbox_button.grid(row=0, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")
    
    chat_button = tk.Button(menu, text="Chat z userem", command=lambda: open_chat_window(menu), width=10,height=2,bg="red")
    chat_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5,sticky="nsew")
    


        
    # Tu umieœæ kod tworz¹cy interfejs logowania, np. pola do wprowadzenia loginu i has³a,
    # przycisk do zatwierdzenia logowania, obs³ugê b³êdów itp.

    menu.mainloop()

if __name__ == "__main__":
    menu_window()
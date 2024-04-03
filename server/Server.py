from fastapi import FastAPI
from pydantic import BaseModel
import random
import requests
from datetime import datetime
import os
import sqlite3

def new_database_operations(cursor):
    cursor.execute('''CREATE TABLE messages
        (
                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 id_sender INT NOT NULL,
                 id_reciver INT NOT NULL,
                 message TEXT NOT NULL,
                 datetime DATETIME NOT NULL,
                 is_read BOOLEAN NOT NULL
        );''')

database_name = 'server/communicator.db'
database_existed = os.path.isfile(database_name)

conn = sqlite3.connect(database_name)
cur = conn.cursor()

if not database_existed:
    new_database_operations(cur)


app = FastAPI()
users = []
unread_messages = []

class User(BaseModel):
    id: int
    name: str
    surname: str

class Message(BaseModel):
    id_sender: int
    id_reciver: int
    message: str
    datetime: datetime | None = None
    is_read: bool

@app.get("/current_users")
def current_users():
    return users

@app.get("/unread_messages_from_user/{id_user}")
def get_unread_messages_from_user(id_user):
    pass

@app.get("/unread_messages")
def get_unread_messages():
    pass

@app.post("/register_user")
async def register_user(user : User):
    user.id = random.randint(1, 9999999) # temporary usage of random library
    users.append(user)
    return user

@app.post("/send_message")
def send_message(message: Message):
    pass

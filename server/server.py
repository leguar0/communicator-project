from fastapi import FastAPI
from pydantic import BaseModel
import random
from datetime import datetime
import os
import sqlite3

def new_database_operations(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS messages
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id_sender INT NOT NULL,
            id_reciver INT NOT NULL,
            message TEXT NOT NULL,
            date_time DATETIME NOT NULL,
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
    date_time: datetime | None = None
    #is_read: bool

@app.get("/current_users")
async def current_users():
    cur.execute('SELECT * FROM users')
    users_data = cur.fetchall()
    users = []
    for user_data in users_data:
        user = {
            "id": user_data[0],
            "name": user_data[1],
            "surname": user_data[2]
        }
        users.append(user)
    return users

@app.get("/unread_messages_from_user/{id_user}")
async def get_unread_messages_from_user(cur_id_user, id_user):
    pass

@app.get("/unread_messages")
async def get_unread_messages(id_user):
    res = cur.execute('SELECT message, date_time, id_sender FROM messages WHERE id_reciver = ? AND is_read = 0', [id_user])
    fetch = res.fetchall()
    if(len(fetch) > 0):
        cur.execute('UPDATE messages SET is_read = 1 WHERE id_reciver = ? AND is_read = 0', [id_user])
        conn.commit()
    return fetch

@app.post("/register_user")
async def register_user(user : User):
    #user.id = random.randint(1, 100) # temporary usage of random library
    cur.execute('INSERT INTO users VALUES(?,?,?)', (user.id,user.name, user.surname))
    conn.commit()
    #users.append(user)
    user.id = cur.lastrowid
    return user

@app.post("/send_message")
async def send_message(m: Message):
    cur.execute('INSERT INTO messages VALUES(NULL,?,?,?,?,False)', (m.id_sender, m.id_reciver, m.message, datetime.now()))
    conn.commit()

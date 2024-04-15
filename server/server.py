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
            id_user INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            username TEXT NOT NULL,       
            password TEXT NOT NULL       
        );''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages
        (
            id_message INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            id_sender INT NOT NULL,
            id_receiver INT NOT NULL,
            message TEXT NOT NULL,
            date_time DATETIME NOT NULL,
            is_read BOOLEAN NOT NULL,
            FOREIGN KEY (id_sender) REFERENCES users(id_user),
            FOREIGN KEY (id_receiver) REFERENCES users(id_user)       
        );''')
    
database_name = 'server/communicator.db'
database_existed = os.path.isfile(database_name)

conn = sqlite3.connect(database_name)
cur = conn.cursor()

if not database_existed:
    new_database_operations(cur)
    
app = FastAPI()
#users = []
unread_messages = []

class User(BaseModel):
    id: int
    name: str
    surname: str
    username: str
    password: str

class Message(BaseModel):
    id_sender: int
    id_receiver: int
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

@app.get("/count_unread_messages_from_user")
async def get_count_unread_messages_from_user(id_sender, id_receiver):
    cur.execute('SELECT id_sender,name,COUNT(*) as total_messages FROM messages INNER JOIN users ON users.id_user = messages.id_sender WHERE id_sender = ? AND id_receiver = ? AND is_read = 0', (id_sender, id_receiver))
    fetch = cur.fetchall()
    return fetch

@app.get("/unread_messages")
async def get_unread_messages(id_user):
    res = cur.execute('SELECT message, date_time, id_sender FROM messages WHERE id_receiver = ? AND is_read = 0', [id_user])
    fetch = res.fetchall()
    if(len(fetch) > 0):
        cur.execute('UPDATE messages SET is_read = 1 WHERE id_receiver = ? AND is_read = 0', [id_user])
        conn.commit()
    return fetch

@app.post("/register_user")
async def register_user(user : User):
    #user.id = random.randint(1, 100) # temporary usage of random library
    cur.execute('SELECT * FROM users WHERE username = ?', [user.username])
    result = cur.fetchone()
    if result is None:
        cur.execute('INSERT INTO users VALUES(NULL,?,?,?,?)', (user.name, user.surname, user.username, user.password))
        conn.commit()
        #users.append(user)
        user.id = cur.lastrowid
        return user
    else:
        return {"registration": False}

@app.post("/login")
async def login_user(user : User):
    cur.execute('SELECT * FROM users WHERE username = ?', [user.username])
    result = cur.fetchone()
    if result:
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (user.username, user.password))
        result = cur.fetchone()
        if result:
            return {"authenticated": True}
    return {"authenticated": False}

@app.post("/send_message")
async def send_message(m: Message):
    cur.execute('INSERT INTO messages VALUES(NULL,?,?,?,?,False)', (m.id_sender, m.id_receiver, m.message, datetime.now()))
    conn.commit()

from calendar import c
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

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
app.add_middleware(CORSMiddleware, allow_origins = ['*'], allow_methods=['*'], allow_headers=["*"])

class User(BaseModel):
    id: int
    name: str | None = ""
    surname: str | None = ""
    username: str | None =  ""
    password: str | None =  ""

class Message(BaseModel):
    id_sender: int
    id_receiver: int
    message: str
    date_time: datetime | None = None
    #is_read: bool

@app.get("/current_users")
async def current_users():
    cur.execute('SELECT id_user, name, surname FROM users')
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
    cur.execute('SELECT COUNT(*) as total_messages FROM messages INNER JOIN users ON users.id_user = messages.id_sender WHERE id_sender = ? AND id_receiver = ? AND is_read = 0', (id_sender, id_receiver))
    fetch = cur.fetchone()
    return fetch[0]

@app.get("/unread_messages")
async def get_unread_messages(id_user):
    res = cur.execute('SELECT message, date_time, id_sender FROM messages WHERE id_receiver = ? AND is_read = 0', [id_user])
    fetch = res.fetchall()
    if(len(fetch) > 0):
        cur.execute('UPDATE messages SET is_read = 1 WHERE id_receiver = ? AND is_read = 0', [id_user])
        conn.commit()
    return fetch

@app.get("/get_messages")
async def get_messages(cur_user, from_user):
    res = cur.execute('SELECT message, date_time, id_sender, id_receiver FROM messages WHERE (id_sender = ? AND id_receiver=?) OR (id_sender=? AND id_receiver = ?)', [cur_user, from_user, from_user, cur_user])
    fetch = res.fetchall()
    #if(len(fetch) > 0):
        #cur.execute('UPDATE messages SET is_read = 1 WHERE id_receiver = ? AND is_read = 0', [id_user])
        #conn.commit()
    print(fetch)
    return fetch

@app.post("/register_user")
async def register_user(user : User):
    cur.execute('SELECT * FROM users WHERE username = ?', [user.username])
    result = cur.fetchone()
    if result is None:
        cur.execute('INSERT INTO users VALUES(NULL,?,?,?,?)', (user.name, user.surname, user.username, user.password))
        conn.commit()
        user.id = cur.lastrowid
        user.password = "" # Let's do not return password ... (tmp solution)
        return user
    else:
        return {"id": -1}

@app.post("/login")
async def login_user(user : User):
    cur.execute('SELECT id_user, name, surname, username FROM users WHERE username = ? AND password = ?', (user.username, user.password))
    result = cur.fetchone()
    if result:
            user = {
                "id": result[0],
                "name": result[1],
                "surname": result[2],
                "username": result[3],
            "password": ""
            }
            return user
    return { "id": -1}

connections: [int, WebSocket] = {}

@app.post("/send_message")
async def send_message(m: Message):
    cur.execute('INSERT INTO messages VALUES(NULL,?,?,?,?,False)', (m.id_sender, m.id_receiver, m.message, datetime.now()))
    conn.commit()
    print(m.id_receiver)
    if m.id_receiver in connections:
        await connections[m.id_receiver].send_text(m.json())
    
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
        await websocket.accept()
    connections[user_id] = websocket
    try:
    while True:
        data = await websocket.receive_text()
            m = Message.parse_obj(json.loads(data))
            await send_message(m)
    except WebSocketDisconnect:
        del connections[user_id]

from calendar import c
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import random
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
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
            password TEXT NOT NULL,
            salt TEXT NOT NULL
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
    cur.execute('SELECT COUNT(*) as total_messages FROM messages WHERE id_sender = ? AND id_receiver = ? AND is_read = 0', (id_sender, id_receiver))
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
    messages = []
    for row in res.fetchall():
        message = {
                "message": row[0],
                "date_time": row[1],
                "id_sender": row[2],
                "id_receiver": row[3]
        }
        messages.append(message)
    if(len(message) > 0):
        cur.execute('UPDATE messages SET is_read = 1 WHERE id_receiver = ? AND id_sender = ? AND is_read = 0', [cur_user, from_user])
        conn.commit()
    return messages

@app.post("/register_user")
async def register_user(user : User):
    cur.execute('SELECT * FROM users WHERE username = ?', [user.username])
    result = cur.fetchone()
    if result is None and len(user.name) >= 3 and len(user.surname) >= 3 and len(user.username) >= 3 and len(user.password) >= 3:
        
        salt = get_random_bytes(16).hex()
        h_user_password = SHA256.new((user.password+salt).encode("utf-8")).digest()
        
        cur.execute('INSERT INTO users VALUES(NULL,?,?,?,?,?)', (user.name, user.surname, user.username, h_user_password, salt))
        conn.commit()
        user.id = cur.lastrowid
        user.password = "" # Let's do not return password ... (tmp solution)
        return user
    else:
        return {"id": -1}

@app.post("/login")
async def login_user(user : User):
    
    cur.execute('SELECT salt FROM users WHERE username = ?', (user.username,))
    result = cur.fetchone()
    if result is None:
        return { "id": -1}

    salt = result[0]
    h_user_password = SHA256.new((user.password+salt).encode("utf-8")).digest()

    cur.execute('SELECT id_user, name, surname, username FROM users WHERE username = ? AND password = ?', (user.username, h_user_password))
    result = cur.fetchone()
    if result:
            user = {
                "id": result[0],
                "name": result[1],
                "surname": result[2],
                "username": result[3],
                "password": "" # Let's do not return password ... (tmp solution)
            }
            return user
    return { "id": -1}

connections = {}

async def send_message(m: Message, wsSender: WebSocket):
    is_connected = False
    if m.id_receiver in connections:
        for id_receiver, ws in connections[m.id_receiver]:
            if id_receiver == m.id_sender:
                await ws.send_text(m.json())
                is_connected = True
        
    for id_receiver, ws in connections[m.id_sender]:
        if (id_receiver == m.id_receiver or id_receiver==m.id_sender) and ws != wsSender:
            await ws.send_text(m.json())
    cur.execute('INSERT INTO messages VALUES(NULL,?,?,?,?,?)', (m.id_sender, m.id_receiver, m.message, datetime.now(), is_connected))
    conn.commit()
    
@app.websocket("/ws/{user_id}/{id_receiver}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, id_receiver: int):
    await websocket.accept()
    if user_id not in connections:
        connections[user_id] = []
    connections[user_id].append((id_receiver, websocket))
    try:
        while True:
            data = await websocket.receive_text()
            m = Message.parse_obj(json.loads(data))
            await send_message(m, websocket)
    except WebSocketDisconnect:
        connections[user_id].remove((id_receiver, websocket))
        if not connections[user_id]:
            del connections[user_id]


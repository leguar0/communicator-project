from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()
users = {}
unread_messages = {}

class User(BaseModel):
    id: int
    name: str
    surname: str

class Message(BaseModel):
    id_sender: int
    id_reciver: int
    message: str
    data: str
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
def register_user(name: str, surname: str):
    pass

@app.post("/send_message")
def send_message(message: Message):
    pass



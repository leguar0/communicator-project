import time
import requests

name = input("Name: ")
surname = input("Surname: ")

user_json = { 
    "id" : 0,
    "name": name,
    "surname": surname
    }

url = 'http://127.0.0.1:8000/register_user'
result = requests.post(url, json = user_json)
print(result.status_code, result.json())
cur_user_id = result.json()["id"]

time.sleep(2)
url = 'http://127.0.0.1:8000/current_users'
print("Current users:")
print(requests.get(url).json())

message = input("Message:")
id_reciver = int(input("to user: "))
if id_reciver != 0:
    url = f'http://127.0.0.1:8000/send_message'
    requests.post(url, json = {"id_sender":cur_user_id, "id_reciver":id_reciver,"message":message})


url = f'http://127.0.0.1:8000/unread_messages?id_user={cur_user_id}'
try:
    while True: 
        res = requests.get(url).json()
        if(len(res) > 0):
            print(res)
        time.sleep(2)
except KeyboardInterrupt:
    pass
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
id_receiver = int(input("to user: "))
if id_receiver != 0:
    url = f'http://127.0.0.1:8000/send_message'
    requests.post(url, json = {"id_sender":cur_user_id, "id_reciver":id_receiver,"message":message})


url = f'http://127.0.0.1:8000/unread_messages?id_user={cur_user_id}'
url2 = f'http://127.0.0.1:8000/count_unread_messages_from_user?id_sender={id_receiver}&id_receiver={cur_user_id}'
try:
    while True:
        response = requests.get(url2)
        res = response.json()
        if len(res) > 0:
            for result in res:
                id_sender = result[0]
                name_sender = result[1]
                total_message = result[2]
                if name_sender != None:
                    print(f"ID_SENDER: {id_sender}, NAME_SENDER: {name_sender}, COUNT: {total_message}")     
            response = requests.get(url)
            res = response.json()
            if len(res) > 0:
                print(res)
            time.sleep(2)
        time.sleep(2)
except KeyboardInterrupt:
    pass
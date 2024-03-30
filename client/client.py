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

url = 'http://127.0.0.1:8000/current_users'

try:
    while True:
        print(requests.get(url).json())
        time.sleep(2)
except KeyboardInterrupt:
    pass
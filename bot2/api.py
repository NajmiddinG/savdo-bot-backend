import requests
import json


BASE_URL = "https://najmiddin.pythonanywhere.com/api"
# BASE_URL = "http://127.0.0.1:8000/api"

def create_user(username, name, user_id):
    url = f"{BASE_URL}/bot_users/"
    data = json.loads(requests.get(url=url).text)
    user_not_exist = True
    for i in data:
        if i["id"] == str(user_id):
            user_not_exist = False
            break
    if user_not_exist:
        try:
            post = requests.post(url=url, data={"id": user_id, "name": name, 'username': username})
            return True
        except: return False
    else: return True

def get_user_language(user_id):
    url = f"{BASE_URL}/bot_users/{user_id}"
    try:
        user = requests.get(url).json()
        return user["lan"]
    except: return 'uz'

def set_user_language(user_id, language):
    url = f"{BASE_URL}/bot_users/{user_id}/"
    try:
        response = requests.patch(url=url, data={"lan": language})
        return response.status_code==200
    except:
        return False
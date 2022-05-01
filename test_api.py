import requests
import json

def get_user(url):
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def create_or_update_user(url,payload):
    payload = json.dumps(payload)
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    return response

def delete_user(url):
    payload={}
    headers = {}
    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response


payload = {
      "checked": True,
      "age": 23,
      "description": "hello",
      "name": "temp"
    }
url = "http://localhost:8080/user/55"

def test_create_update():
    get_res = get_user(url)
    if get_res.status_code == 404:
        put_res = create_or_update_user(url,payload)
        assert put_res.status_code == 201
    elif get_res.status_code == 200:
        put_res = create_or_update_user(url,payload)
        assert put_res.status_code == 200

def test_read_delete():
    get_res = get_user(url)
    if get_res.status_code == 200:
        del_res = delete_user(url)
        assert del_res.status_code == 204
    elif get_res.status_code == 404:
        assert del_res.status_code == 404

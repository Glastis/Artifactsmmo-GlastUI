import json
import requests

from constants import account, api

def remove_duplicate_slashes(url):
    while "//" in url:
        url = url.replace("//", "/")
    return url

def make_url(uri):
    url = f"{api.base_url}/{uri}"
    url = remove_duplicate_slashes(url)
    url = f'{api.protocol}://{url}'
    return url

def request(uri, method, data=None):
    url = make_url(uri)
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {account.token}'
    }
    if method == "POST":
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, headers=headers, data=json.dumps(data))
    elif method == "GET":
        response = requests.get(url, headers=headers)
    else:
        print(f"Invalid method: {method}")
        return None

    if response.status_code != 200:
        print(f"Request {url} failed: {response.status_code}, {response.text}")
        return None
    data = response.json()
    return data['data']

def post(uri, data=None):
    return request(uri, "POST", data)


def get(uri):
    return request(uri, "GET")

def post_action(hero_name, action, data=None):
    return post(f'{hero_name}/actions/{action}', data)
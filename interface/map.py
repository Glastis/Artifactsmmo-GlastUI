import json

import interface.request as request

map_data = None

def update_map_data():
    global map_data
    all_data = []
    data_pages = []
    page = 1
    size = 100
    while True:
        response = request.request(f"/maps?page={page}&size={size}", "GET", return_all=True)
        response = response.json()
        all_data.extend(response['data'])
        data_pages.append(response['data'])
        if page >= response['pages']:
            break
        page += 1
    map_data = all_data

def get_map_data():
    if not map_data:
        update_map_data()
    return map_data
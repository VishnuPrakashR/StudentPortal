import json

import requests


class Request:
    def __init__(self):
        f = open('API/Gateway.json', 'r')
        api = json.load(f)
        self.url = api.get('URL')

    def get_api(self, path='', method="GET", data={}, headers={}):
        url = f'{self.url}/{path}'
        apiResponse = requests.request(method, url, headers=headers, data=data)
        response = apiResponse.text
        return response

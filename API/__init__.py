#  Copyright (c) 2023. This is the property of Vishnu Prakash
import json


class verification:
    def __init__(self):
        f = open('API/ApiKey.json', 'r')
        api = json.load(f)
        self.apiKey = api.get('X-API-Key')
        self.referer = api.get('Referer')

    def verify(self, apiKey, referer):
        if referer == self.referer:
            if apiKey == self.apiKey:
                return {"Verified": True}
            else:
                return {"Verified": False, "Msg": "Wrong API Key"}
        else:
            return {"Verified": False, "Msg": "Wrong Referer"}

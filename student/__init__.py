import json

from API.Request import Request


class API(Request):
    def __init__(self):
        super().__init__()

    def request_current(self, headers):
        response = self.get_api(path='user/student/current', headers=headers)
        current_user = json.loads(response)
        return current_user.get("StudentId")

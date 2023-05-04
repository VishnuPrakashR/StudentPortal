from . import API


class Dashboard(API):
    def __init__(self):
        super().__init__()

    def Data(self, headers):
        current_user = self.request_current(headers)

        return {"CurrentUser": current_user}

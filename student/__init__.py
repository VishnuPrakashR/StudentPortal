import json
from datetime import date, timedelta, datetime

from bson import ObjectId

from API.Request import Request
from db import Mongo


class API(Request):
    def __init__(self):
        self.studentId = None
        self.amount = None
        self.invoiceType = None
        self.invoices = Mongo('invoices')
        super().__init__()

    def request_current(self, headers):
        response = self.get_api(path='user/student/current', headers=headers)
        current_user = json.loads(response)
        return current_user.get("studentId")

    def user_register(self, email, password, studentId):
        formData = {
            "email": email,
            "password": password,
            "studentId": studentId
        }
        response = self.get_api(path='user/student/register', data=formData, method='POST')
        apiResponse = json.loads(response)
        return apiResponse

    def create_finance_account(self, studentId):
        formData = {
            "studentId": studentId
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.get_api(path='finance/accounts/', formJson=formData, method='POST', headers=headers)
        apiResponse = json.loads(response)
        return apiResponse

    def create_library_account(self, studentId):
        formData = {
            "studentId": studentId
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.get_api(path='library/api/register', formJson=formData, method='POST', headers=headers)
        apiResponse = json.loads(response)
        return apiResponse

    def create_invoice(self):
        dueDate = date.today() + timedelta(days=10)
        formData = {
            "amount": self.amount,
            "type": self.invoiceType,
            "dueDate": datetime.strftime(dueDate, "%Y-%m-%d"),
            "account": {"studentId": self.studentId}
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.get_api(path='finance/invoices/', formJson=formData, method='POST', headers=headers)
        apiResponse = json.loads(response)
        refNum = apiResponse.get("reference")
        invoice = {
            "Reference": refNum,
            "StudentId": self.studentId,
            "Amount": self.amount,
            "Type": self.invoiceType,
            "Status": 1,
            "IsPaid": False
        }
        invoiceResult = self.invoices.put(invoice)
        apiResponse.update({
            "invoiceId": format(invoiceResult.inserted_id)
        })
        return apiResponse

    def checkIsPaidInvoice(self, reference, Id):
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.get_api(path=f'finance/invoices/reference/{reference}',  method='GET', headers=headers)
        apiResponse = json.loads(response)
        if apiResponse.get('status') == 'PAID':
            result = self.invoices.set({"_id": ObjectId(Id)}, {"IsPaid": True})
            return True
        else:
            return False

    def payInvoice(self, reference):
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.get_api(path=f'finance/invoices/{reference}/pay', method='PUT', headers=headers)
        apiResponse = json.loads(response)
        return apiResponse

    def hasOutstanding(self, studentId):
        headers = {
            'Content-Type': 'application/json'
        }
        response = self.get_api(path=f'finance/accounts/student/{studentId}', method='GET', headers=headers)
        apiResponse = json.loads(response)
        return apiResponse.get('hasOutstandingBalance')



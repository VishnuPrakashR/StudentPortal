from bson import ObjectId

from . import API
from db import Mongo

enrollNo = Mongo('numbering')


class Fees(API):
    def __init__(self, headers):
        super().__init__()
        self.current_user = self.request_current(headers)

    def All(self):
        feesData = self.invoices.get({"StudentId": self.current_user})
        response = []
        for i, fees in enumerate(feesData, 1):
            reference = fees.get('Reference')
            if fees.get('IsPaid'):
                data = {
                    "isPaid": True
                }
            else:
                if self.checkIsPaidInvoice(reference, fees.get('_id')):
                    data = {
                        "isPaid": True
                    }
                else:
                    data = {
                        "isPaid": False
                    }
            data.update({
                "No": i,
                "Reference": reference,
                "Amount": fees.get('Amount'),
                "Type": fees.get('Type'),
                "Id": format(fees.get('_id')),
                "Status": fees.get('Status')
            })
            response.append(data)
        return response

    def Pay(self, formData):
        reference = formData.get("reference")
        apiResponse = self.payInvoice(reference)
        if apiResponse.get("status") == "PAID":
            result = self.invoices.set({"Reference": reference}, {"IsPaid": True})
            response = {
                "Response": "Success",
                "Msg": "Invoice paid successfully"
            }
        else:
            response = {
                "Response": "Error",
                "Msg": "Some sort of error happened"
            }, 400
        return response

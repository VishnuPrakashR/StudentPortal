from . import API
from db import Mongo

regNumber = Mongo('numbering')
studentTable = Mongo('students')


class Register(API):
    def __init__(self):
        super().__init__()
        self.type = 'student'

    def register(self, data):
        studentId = self.new_student_id()
        studentData = {
            "Name": data.get('fullname'),
            "Email": data.get('email'),
            "Dob": data.get('dob'),
            "Address": data.get('address'),
            "Country": data.get('country'),
            "PostCode": data.get('postcode'),
            "Phone": data.get('phonenumber'),
            "StudentId": studentId
        }
        result = studentTable.put(studentData)
        response = self.user_register(data.get('email'), data.get('password'), studentId)
        accounts = self.create_finance_account(studentId)
        library = self.create_library_account(studentId)
        response.update({
            "Response": "Success",
            "insertID": format(result.inserted_id),
            "accountResponse": accounts,
            "libraryResponse": library
        })
        return response

    def new_student_id(self):
        currentNum = regNumber.getaftercount({'type': self.type, 'status': 1}, 'studentId')
        newNum = 'c' + format(currentNum.get('studentId')).zfill(6)
        return newNum

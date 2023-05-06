from bson import ObjectId

from . import API
from db import Mongo

enrollNo = Mongo('numbering')


class Enrollment(API):
    def __init__(self, headers):
        self.students = Mongo('students')
        self.enrollment = Mongo('enrollment')
        self.courses = Mongo('courses')
        super().__init__()
        self.current_user = self.request_current(headers)
        self.type = "enrollment"

    def Enroll(self, formData):
        enrollmentNo = self.new_enrollment_no()
        data = {
            "EnrollmentNo": enrollmentNo,
            "StudentId": self.current_user,
            "Course": ObjectId(formData.get("course")),
            "IsGraduated": False,
            "Status": 1
        }
        result = self.enrollment.put(data)
        courseData = self.courses.getone({"_id": ObjectId(formData.get("course"))})
        self.invoiceType = "TUITION_FEES"
        self.amount = courseData.get("Fees")
        self.studentId = self.current_user
        apiResponse = self.create_invoice()
        response = {
            "Response": "Success",
            "RequestId": format(result.inserted_id),
            "invoiceId": format(apiResponse.get("reference"))
        }
        return response

    def new_enrollment_no(self):
        currentNum = enrollNo.getaftercount({'type': self.type, 'status': 1}, 'enrollmentNo')
        newNum = currentNum.get('enrollmentNo')
        return newNum

    def Data(self):
        data = self.enrollment.getone({"StudentId": self.current_user})
        if data:
            courseData = self.courses.getone({"_id": ObjectId(data.get("Course"))})
            studentData = self.students.getone({"StudentId": self.current_user})
            response = {
                "Response": "Success",
                "enrolled": True,
                "enrollmentNo": data.get("EnrollmentNo"),
                "Course": courseData.get("CourseName"),
                "Degree": courseData.get("CourseCategory"),
                "Fees": courseData.get("Fees"),
                "IsGraduated": data.get("IsGraduated"),
                "CourseLeader": courseData.get("CourseLeader"),
                "Name": studentData.get("Name"),
                "Email": studentData.get("Email"),
                "studentId": studentData.get("StudentId"),
                "Phone": studentData.get("Phone"),
                "Dob": studentData.get("Dob"),
                "Address": studentData.get("Address"),
                "PostCode": studentData.get("PostCode"),
                "Country": studentData.get("Country")
            }
            if data.get("IsGraduated"):
                response.update({
                    "FeesPaid": True
                })
            else:
                if self.hasOutstanding(self.current_user):
                    response.update({
                        "FeesPaid": False
                    })
                else:
                    response.update({
                        "FeesPaid": True
                    })
        else:
            courses = self.courses.get({"Status": 1})
            allCourses = []
            for course in courses:
                courseData = {
                    "Id": format(course.get("_id")),
                    "Course": course.get("CourseName"),
                    "Degree": course.get("CourseCategory")
                }
                allCourses.append(courseData)
            response = {
                "Response": "Success",
                "enrolled": False,
                "courses": allCourses
            }
        return response

    def Graduate(self, formData):
        result = self.enrollment.set({"EnrollmentNo": int(formData.get("enrollmentNo"))}, {"IsGraduated": True})
        response = {
            "Response": "Success",
            "Msg": "Student graduated successfully"
        }
        return response

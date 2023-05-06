from bson import ObjectId

from . import API
from db import Mongo


class Dashboard(API):
    def __init__(self, headers):
        self.students = Mongo('students')
        self.enrollment = Mongo('enrollment')
        self.courses = Mongo('courses')
        super().__init__()
        self.current_user = self.request_current(headers)

    def Data(self):
        data = self.students.getone({"StudentId": self.current_user})
        response = {
            "Id": format(data.get("_id")),
            "Name": data.get("Name"),
            "Email": data.get("Email"),
            "studentId": data.get("StudentId"),
            "Phone": data.get("Phone"),
            "Dob": data.get("Dob"),
            "Address": data.get("Address"),
            "PostCode": data.get("PostCode"),
            "Country": data.get("Country")
        }
        return response

    def EnrollData(self):
        data = self.enrollment.getone({"StudentId": self.current_user})
        if data:
            courseData = self.courses.getone({"_id": ObjectId(data.get("Course"))})
            response = {
                "Response": "Success",
                "enrolled": True,
                "enrollmentNo": data.get("EnrollmentNo"),
                "Course": courseData.get("CourseName"),
                "Degree": courseData.get("CourseCategory"),
                "Fees": courseData.get("Fees"),
                "IsGraduated": data.get("IsGraduated"),
                "CourseLeader": courseData.get("CourseLeader")
            }
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

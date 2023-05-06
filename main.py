#  Copyright (c) 2023. This is the property of Vishnu Prakash
from flask import Flask, request, jsonify
from flask_cors import CORS

from API import verification
from student import Dashboard, Register, Course, Fees

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config.update(
    SECRET_KEY=b'\xa8G\x1c\x84@EQ\xdd\xa2\xf8\xe2\xed\x9e\x9ft\x8f'
)
CORS(app, expose_headers="content-disposition", supports_credentials=True)


@app.route("/")
def hello():
    return "Student Portal API"


@app.route('/register/', methods=['POST'])
def register():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Register.Register().register(request.form)
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Dashboard/Data/', methods=['GET', 'POST'])
def dashboard():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Dashboard.Dashboard(request.headers).Data()
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Dashboard/Enroll/', methods=['GET', 'POST'])
def enroll_data():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Dashboard.Dashboard(request.headers).EnrollData()
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Course/Enroll/', methods=['POST'])
def enroll():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Course.Enrollment(request.headers).Enroll(request.form)
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Fees/', methods=['GET', 'POST'])
def all_fees():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Fees.Fees(request.headers).All()
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Fees/Pay/', methods=['POST'])
def pay_fees():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Fees.Fees(request.headers).Pay(request.form)
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Course/EnrollmentData/', methods=['GET', 'POST'])
def enrollment_data():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Course.Enrollment(request.headers).Data()
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


@app.route('/Course/Graduate/', methods=['POST'])
def graduate():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Course.Enrollment(request.headers).Graduate(request.form)
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


def run():
    app.run(host="0.0.0.0", port=5003, debug=True, load_dotenv='development')


if __name__ == "__main__":
    run()

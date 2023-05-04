#  Copyright (c) 2023. This is the property of Vishnu Prakash
from flask import Flask, request, jsonify
from flask_cors import CORS

from API import verification
from student.Dashboard import Dashboard

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config.update(
    SECRET_KEY=b'\xa8G\x1c\x84@EQ\xdd\xa2\xf8\xe2\xed\x9e\x9ft\x8f'
)
CORS(app, expose_headers="content-disposition", supports_credentials=True)


@app.route("/")
def hello():
    return "Student Portal API"


@app.route('/Dashboard/Data/', methods=['GET', 'POST'])
def dashboard():
    apiKey = request.headers.get("X-API-Key")
    referer = request.headers.get("Referer")
    apiResponse = verification().verify(apiKey, referer)
    if apiResponse.get("Verified"):
        response = Dashboard().Data(request.headers)
    else:
        response = jsonify({"Response": apiResponse.get("Msg")}), 401
    return response


def run():
    app.run(host="0.0.0.0", port=5003, debug=True, load_dotenv='development')


if __name__ == "__main__":
    run()

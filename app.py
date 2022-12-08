from src.label import main

from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


env_file = find_dotenv(".env.dev")
load_dotenv(env_file)


@app.route("/", methods=["POST", "OPTIONS"])
@cross_origin(supports_credentials=True)
def home():
    print("request -- ", request.get_json())
    res = main(request.get_json())

    return res


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)

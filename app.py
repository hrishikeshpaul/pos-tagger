
from label import main

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def home():
    res = main(request.get_json())
    return res

if __name__ == '__main__':
    app.run(threaded=True, port=5000, debug=True)

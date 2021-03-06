import threading

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from Handler import Handler

app = Flask(__name__)
CORS(app)


def process(data):
    handler = Handler(data).start()


@app.route("/")
def hello():
    return "Cropper backend working!"


@app.route("/processing", methods=['POST'])
@cross_origin()
def index():
    print(request.json)
    threading.Thread(target=process, args=[request.json['data']]).start()
    return jsonify(request.json)


@app.route("/rotate", methods=['POST'])
@cross_origin()
def rotate():
    return jsonify(Handler(None).rotate(request.json))


@app.route("/make-preview", methods=['POST'])
@cross_origin()
def make_preview():
    Handler(None).make_preview(request.json)
    return jsonify(request.json)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)

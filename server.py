from flask import Flask, request, jsonify
from PIL import Image, ImageOps
from Cropper import Cropper
from Handler import Handler
import json

app = Flask(__name__)

imageObject = Image.open("./test.jpg")
width, height = imageObject.size
cropped = imageObject.crop((width / 2, height / 2, width, height))
cropped.save('./test3.jpg')

ImageOps.expand(cropped, border=30, fill='#FF0000').resize((int(width - width / 2), int(height - height / 2)),
                                                           Image.ANTIALIAS).save('test2.jpg')

cropper = Cropper('test.jpg')
# cropper.start_processing()

handler = Handler([{"url": "test.jpg", "crop": "true"}, {"url": "test2.jpg", "crop": "true"}])
handler.start()

@app.route("/")
def hello():
    i = 0
    print("incoming request")
    while i < 100:
        handler2 = Handler([{"url": "test.jpg", "crop": "true"}, {"url": "test2.jpg", "crop": "true"}])
        handler2.start()
        i += 1
    return "Hello World!"


@app.route("/processing", methods=['POST'])
def index():
    data = request.json
    print(data)
    handler1 = Handler(data)
    handler1.start()
    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)

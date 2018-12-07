from flask import Flask,request,jsonify
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS
from face_classification.src.image_emotion_gender_dec import gender_emotion_dec
import time
import os

app = Flask(__name__)
CORS(app)

@app.route('/test',methods=['POST','GET'])
def test():
    return "test success"

@app.route('/',methods=['POST','GET'])
def hello_world():
    file = request.form['image']
    starter = file.find(',')
    image_data = file[starter + 1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))

    img_name = str(time.time()).replace('.', 'a') + '.png'
    img_path = os.path.join('./', img_name)
    im.save(img_path)
    ge = gender_emotion_dec(img_path)
    print(ge)
    
    if ge[0] == "":
    	return jsonify(emotion = "", emotion_probability= "", gender="",gender_probability = "",code =0)
    else:
    	return jsonify(emotion = ge[0], emotionp= ge[2], gender=ge[1] ,genderp = ge[3] ,code=1)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8889')

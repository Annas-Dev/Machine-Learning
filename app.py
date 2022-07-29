from multiprocessing.sharedctypes import Value
from PIL import Image
import numpy as np
#load the trained model to classify sign
from keras.models import load_model
from flask import Flask, render_template, request
from rsa import sign
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
model = load_model('ModelTrafficSignIndo.h5')

#dictionary to label all traffic signs class.
classes = { 1: 'Ada pekerjaan di jalan',
            2: 'bahaya longsoran tanah',
            3: 'Di depan jalan buntu',
            4: 'Dilarang Klakson',
            5: 'Dilarang Masuk',
            6: 'Gerbang Tol',
            7: 'Gereja',
            8: 'Hati-hati, mohon kendaraan pelan',
            9: 'Jalur Evakuasi Gempa Bumi',
            10: 'Jalur Evakuasi Gunung Merapi',
            11: 'Jalur Evakuasi Tsunami',
            12: 'Larangan bagi pejalan kaki',
            13: 'Larangan bagi sepeda',
            14: 'Larangan masuk bagi mobil dan motor',
            15: 'Larangan mobil',
            16: 'Larangan sepeda motor',
            17: 'Masjid',
            18: 'Pura',
            19: 'Rumah Sakitn',
            20: 'Rawan Kecelakaan',
            21: 'Wihara' }
               

# the input image is required to be in the shape of dataset, i.e (32,32,3)
 

#hasil = pred,classes[max(range(len(pred)), key = lambda x: pred[x])]
#print(pred,classes[max(range(len(pred)), key = lambda x: pred[x])])



app = Flask(__name__)
UPLOAD_FOLDER = 'Uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html", value="")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return index()
    elif request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        im=Image.open(filePath)
        im = im.resize((30,30))
        im=img_to_array(im) 
        im=im/255.0
        im = np.array(im)
        im = np.expand_dims(im, axis=0)
        #print(image.shape)
        pred = model.predict([im])[0]
        #return 'file uploaded successfully'

        # image = image.resize((30,30))
        # image = np.expand_dims(image, axis=0)
        # image = np.array(image)
        # print(image.shape)
        # pred = model.predict([image])[0]
        sign = classes[max(range(len(pred)), key = lambda x: pred[x])]
        return render_template("index.html", value=sign)
    

if __name__ == "__main__":
    app.run(debug=True)
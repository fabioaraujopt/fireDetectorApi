from flask import Flask
from flask import render_template
from flask import request, flash, redirect
from werkzeug.utils import secure_filename
import os
import sys
import json
import time

sys.path.insert(0, '../Mask_RCNN')

from MaskDetector import FireDetector
import utils


fire_detector = FireDetector('../trained_weights')

UPLOAD_FOLDER = 'saved_img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','tif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24) 


#keys may be ['rois','scores','class_ids','masks','time']       
def jsonParse (result,keys):
    response={}
    for key in keys:
        try:
            response[key]= result[key].tolist()
        except:
            response[key]= result[key]
    return (response)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/',methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        arrival_time = time.time()
        if 'fire_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['fire_image']
        if file.filename == '':
            flash('No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = utils.getGpsData('/home/fctmasterthesis/fire_app/saved_img/'+filename)
            img_id=utils.convertImage('/home/fctmasterthesis/fire_app/saved_img/'+filename)
            #result=fire_detector.detect('/home/fctmasterthesis/fire_app/converted_images/'+img_id)
            #result= jsonParse(result,['rois','scores','class_ids','time'])
            #result['arrival_time']=arrival_time
            return json.dumps([data,img_id])         
            #return json.dumps(result)

    return render_template('upload.html')

app.run(host='0.0.0.0',port='5000')


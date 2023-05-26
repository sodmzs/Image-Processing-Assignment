from distutils.log import debug
from fileinput import filename
from flask import *  
from configparser import ConfigParser
from utils import detect_gun, inpainting_detected_gun, smile_expression, replacing_gun_with_musical_instrument
from roboflow import Roboflow
import cv2
import numpy as np
from PIL.Image import Image
import io
import base64
import os

app = Flask(__name__)  
  
@app.route('/')  
def main():  
    return render_template("index.html")  
  
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        isExist = os.path.exists("Input File")
        if not isExist:
           os.makedirs("Input File")
        f.save("Input File/"+f.filename)
        filename = "Input File/"+f.filename
        instrument_file = "musical instrument/tuba.png"
        temp_path = "Temp"

        isExist = os.path.exists(temp_path)
        if not isExist:
           os.makedirs(temp_path)

        config = ConfigParser()
        print (config.read('config.ini'))

        res = detect_gun(filename)
        cv2.imwrite(temp_path+"/gun_detected.png",res)

        file, msg = inpainting_detected_gun(filename,temp_path+"/gun_detected.png")
        print("!!! ",msg)

        file, msg = smile_expression(temp_path+"/"+file)
        print("!!! ",msg)

        res = replacing_gun_with_musical_instrument(temp_path+"/"+file,temp_path+"/gun_detected.png",instrument_file)
        isExist = os.path.exists("Output")
        if not isExist:
           os.makedirs("Output")
        cv2.imwrite("Output/final.png",res)
        #f.save(f.filename)  
        return render_template("index.html", name = f.filename)  
  
if __name__ == '__main__':  
    app.run(debug=True)

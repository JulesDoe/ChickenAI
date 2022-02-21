from flask import Flask
from flask import jsonify
import tensorflow as tf
from tensorflow import keras
import logging
import requests
from datetime import datetime
import numpy as np

from PIL import UnidentifiedImageError

logging.basicConfig(level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')

# logging.basicConfig(filename='log.log',
#                     filemode='a',
#                     level=logging.INFO,
#                     format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')



# Image Downloader
imgURL = "http://192.168.178.64/snapshot.jpg"

def getImg():
    try:
        req = requests.get(imgURL, timeout=5)
        img_data = req.content
        logging.info(f"{req.status_code} {req.elapsed}")


        file = f'D:\chickenAI\{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg'
        logging.info(file)
        with open(file, 'wb') as handler:
            handler.write(img_data)
        
        return file
    
    except requests.exceptions.ReadTimeout:
        logging.error(f"Timeout")
    except requests.exceptions.ConnectionError:
        logging.error(f"Timeout")
    except Exception as e:
        logging.error('%s', exc_info=e)
    return None

# Model
model = keras.models.load_model('../model/model.h5')

img_height= 60
img_width = 60

class_names = ['chicken', 'egg', 'empty']

def predict(imageFile):
    try:
        img = keras.preprocessing.image.load_img(
            imageFile, target_size=(img_height, img_width)
        )
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])

        # print(
        #     "This image most likely belongs to {} with a {:.2f} percent confidence."
        #     .format(class_names[np.argmax(score)], 100 * np.max(score))
        # )
        bla = {
            "class":class_names[np.argmax(score)],
            "probability":100 * np.max(score)
            }
    except UnidentifiedImageError as e:
        logging.warn(f"Wierd Image {imageFile} {e}")
        bla = None


    return bla


# Server
app = Flask(__name__)

@app.route('/')
def magick():

    img = getImg()

    if img: #is not None
        res = predict(img)
        if res:
            print(res)
            return jsonify(res)

    # else img is None
    return jsonify({"Debug":  f"{imgURL} not available"}) , 502


# Runn it
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
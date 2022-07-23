from cmath import log
import sys
import requests
import urllib3
import logging
from time import time, sleep
from datetime import datetime

img_file_path = "/home/pi/training/"
# img_file_path = "D:/chickenAI/test/"

logging.basicConfig(filename='datalog.log',
                    filemode='a',
                    level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')

while True:
    if datetime.now().hour >= 7 and datetime.now().hour < 12:
        try:
            req = requests.get("http://192.168.178.64/snapshot.jpg", timeout=10)
            img_data = req.content
            logging.info(f"Request status:{req.status_code} duration:{req.elapsed} bytes recieved:{len(img_data)}")

            if len(img_data) > 0: #saving an image only when actual data comes back
                file = f'{img_file_path}{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg'
                logging.info(file)
                with open(file, 'wb') as handler:
                    handler.write(img_data)
            else:
                logging.error(f"{len(img_data)} bytes recieved.") # This usualy means the ESP-Cam is available but the webserver doesnt deliver an image.
                logging.info("Faking a stream user by requesting esp cam front page")
                req = requests.get("http://192.168.178.64", timeout=10)
                logging.info(f"Request status:{req.status_code} duration:{req.elapsed} bytes recieved:{len(img_data)}")

        
        except KeyboardInterrupt:
            sys.exit()

        except requests.exceptions.ReadTimeout:
            logging.error(f"Read Timeout")
            logging.info(f"status:{req.status_code} duration:{req.elapsed} bytes recieved:{len(req.content)}")

        # except requests.exceptions.ConnectionError:
        #     logging.error(f"Connection Error")
        #     logging.info(f"status:{req.status_code} duration:{req.elapsed} bytes recieved:{len(req.content)}")

        except Exception as e:
            logging.error('%s', exc_info=e)
    else:
        logging.info('wrong time to take a picture; waiting 1h')
        sleep(3600)
        
    # regular sleep between images
    sleep(10)

    

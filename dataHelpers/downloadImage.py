import sys
import requests
import urllib3
import logging
from time import time, sleep
from datetime import datetime

img_file_path = "/home/pi/training/"

logging.basicConfig(filename='datalog.log',
                    filemode='a',
                    level=logging.INFO,
                    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')

while True:
    if datetime.now().hour >= 7 and datetime.now().hour < 12:
        try:
            req = requests.get("http://192.168.178.64/snapshot.jpg", timeout=10)
            img_data = req.content
            logging.info(f"{req.status_code} {req.elapsed}")

            # home = os.path.expanduser('~')
            file = f'{img_file_path}{datetime.now():%Y-%m-%d-%H-%M-%S}.jpg'
            logging.info(file)
            with open(file, 'wb') as handler:
                handler.write(img_data)
            
            #sleep(1.5)
        
        except KeyboardInterrupt:
            sys.exit()
        except requests.exceptions.ReadTimeout:
            logging.error(f"Timeout")
        except requests.exceptions.ConnectionError:
            logging.error(f"Timeout")

        except Exception as e:
            logging.error('%s', exc_info=e)
    else:
        logging.info('wrong time to take a picture')
    sleep(10)

    

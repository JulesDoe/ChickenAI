# 🐔 What is this 
If home automation is your thing and you have chickens - You for shour asked your self the question:
"Wy cant my Digital Assistend tell me if there are eggs i could get for making my sunday breckfast?"
And for shour you came to the conclusion .. well my chickens lay more or less the same amount of eggs day after day.

We came to the conclusion there should be Tech for this!
So - we build it. An ESP-Cam - AI - Webservice - that integrates in your Home automation systhems.
To enable the tech saby user to triger whatever home automation if there is a fresh warm egg. 

# 🐤 But does it work?
Well... we havent deployed it __in production__ yet. But each component on its on seems to work fine in oure testing.

# 🐥 How does it work
We installed a ESP-Cam over the nest where the chickens usualy lay there eggs.
We had it take thousands of pictures from dawn to dusk.
Sorted out the to dark ones with a script.
Labeld them by hand sorting them into thre category folders (chicken / egg / empty).
And ran them through a lightley modified version of the the tensorflow example for classifier.
This trained model is made available though a webservice running on a RaspberyPi3.
Node-Red accesses the webservice for any home automation flows.
And finaly a Apple Home Pod anounces there is a dangerously high concentration of CO2 in the Nest (sounds like an egg to my ears!)

## hardware
An ESP-Cam was flashed with the Tasmota firmware. 
It was installed roughly 50 cm above the Nest. We tok care to have the whole nest in frame.
The esp cam in oure case spit out images with differend kinds of defects. We catch the worst of them later on in exeption handling.

## image recorder
To generate training data we use the `downloadImage.py` script. The service `chickpic.service` takes care of restarting the python script after a reboot. 
Create the service:
```
sudo nano /etc/systemd/system/chickpic.service
```

And add the following content to the file:

```
[Unit]
Description=My test service
After=multi-user.target
[Service]
Type=simple
WorkingDirectory = /home/pi/
Restart=always
ExecStart=/usr/bin/python3 /home/pi/ChickenAI/dataHelpers/downloadImage.py
[Install]
WantedBy=multi-user.target
```
To load, enable and start the service:

```
sudo systemctl daemon-reload
sudo systemctl enable chickpic.service
sudo systemctl start test.service
````
After making changes to the python script you have to stop and restart the service:
```
sudo systemctl stop chickpic.service
sudo systemctl start chickpic.service
```

This service will now download a picture every 10 seconds from one of the webcams and saves them in the `pi/training` directory. The log file of this service can be found in `pi/datalog.log`. 

### dataHelpers
These helper scripts were created in attempts to filter out unusable data. `checkBrightnes.py` proved most usefull. `imageDifference.py` was a try in sinmple motion detection to throw away images where nothing happens. But for not we actualy have a lot of these "nothing happens" images in oure actual training data to balance the classes of the dataset as this greatly improved the accuracy. `countPixelColors.py` was used to discover the defect images coming from the ESP-Cam.  


## classifier
As a classifier we took the tensorflow example calassifier and modified it lightly.
Obviously we had it load oure own dataset.
We also modified the size of images from 180x180 to 60x60
The CPU training of the classifier took around a minut on a Laptop with 8Gen 6 Core i7.
![example Image of dataset ](/docs/dataset.png)


## server
The server runns a flask aplication that has one single endpoint on a RaspberyPi 3. If it recieves a request it sends itself a request to the ESP-Cam which responds with a jpeg. If a uncorupted jpeg was recieved, it gets passed to the tensorflow model and the results are send out as JSON.

## Automation with Node RED
We build a simple Flow that triggers every minute and lets the webservice to do its thing. And than pass the result on.  

## Automation in Apple Home app
We found a quite hacky way to play sounds with the Apple Home App to our harts contend. Since we cant create a new Sensor type we repurpused an existing one (CO2) and programmed it to play a short pice of musik from Apple Music if this Sensor goes to its Alarm state (this seems to be the only way to "push" notifi devices). 

## Model exporter
__for historic purposes__ We wanted to run the model directly in Node RED at first. So we converted it to the tensorflow.js JSON format.
There is a hacky way to load generic tensorflow.js models in Node-RED with a bit of JavaScript glue nodes. We exported oure model to work with that, but later on decidet to put the model evaluation in a seperate web-app because it seemt somewat augward to force Node-RED to do souch things.


# 🐣 I Want it

## Workflow
- setup hardware
- collect data
- lable data
- train classifier on your data
- setup webservice
- setup Node Red
- setup your Automations

## Envoirement
We use conda becaus it suposidly makes the installation of Tensorflow-GPU easy... but we didnt got it to work. Probably because of the wrong installation order, since conda and pip dont work well togehter there yet and there keept coming up problems around the numpy version.

So its pip only.
```
conda create -n chicken python=3.9
pip install tensorflow
conda install ipykernel --update-deps
pip install tqdm
pip install flask
pip install paho-mqtt
```

### tfjs export
__for historic purposes__
This needs a different envoirment since its recomendet and running in python 3.6
conda create -n tfjs python=3.6.8

we created the following command through the `tensorflowjs_wizard`
`tensorflowjs_converter --input_format=keras --metadata= --output_format=tfjs_layers_model --weight_shard_size_bytes=4194304 model/model.h5 model/export`

# 🐓 License
(of course) Chicken Dance License v0.2


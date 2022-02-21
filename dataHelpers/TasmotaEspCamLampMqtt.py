from dataHelpers.secrets import SSID, WifiPassword
import paho.mqtt.client as paho
import mySecrets
from time import sleep

broker= mySecrets.mqttBrockerIP
port= mySecrets.mqttBrockerPort
def on_publish(client,userdata,result):  #create function for callback
    # print(client,userdata,result)
    # print("data published \n")
    pass

client1= paho.Client("control1")         #create client object
client1.username_pw_set(username= mySecrets.SSID, password= mySecrets.WifiPassword)
client1.on_publish = on_publish          #assign function to callback
client1.connect(broker,port)             #establish connection

while True:
    ret= client1.publish("cmnd/chick_cam_02/Power","TOGGLE") #publish
    sleep(1.0)
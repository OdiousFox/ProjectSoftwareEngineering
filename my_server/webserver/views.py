
from django.shortcuts import render
from django.http import HttpResponse

from .models import DeviceType
from .models import Device
from .models import PyEntries
from .models import LhtEntries

import paho.mqtt.client as mqtt
import time

import messageFormatter




def my_view(request, *args, **kwargs):
    
    # Iterate through all the data items
    
    DeviceType.objects.create("py", "pycom","battery powered, time, temperature, light, pressure")
    DeviceType.objects.create("lht", "lhtcom","plugIn, time, temperature, light, Humidity, workmode, batteryVoltage")
    
    Device.objects.create("py-saxion", "py", "M.H. Tromplaan 28, 7513 AB, Enschede, Netherlands")
    Device.objects.create("py-wierden", "py", "Burgemeester J.C. van Den Bergplein 17-18, 7642 GS, Wierden")
    Device.objects.create("lht-gronau", "lht", "48599 Gronau, North Rhine-Westphalia, Germany")
    Device.objects.create("lht-wierden", "lht", "Burgemeester J.C. van Den Bergplein 17-18, 7642 GS, Wierden")
    Device.objects.create("lht-saxion", "lht", "M.H. Tromplaan 28, 7513 AB, Enschede, Netherlands")

    client()

def client():
    username = "project-software-engineering@ttn"
    password = "NNSXS.DTT4HTNBXEQDZ4QYU6SG73Q2OXCERCZ6574RVXI.CQE6IG6FYNJOO2MOFMXZVWZE4GXTCC2YXNQNFDLQL4APZMWU6ZGA"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("extapi/data/esm")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        messageFormatter.formatMessage
        global values = messageFormatter.returnMessage(msg.payload)
        if "py" in values[0]:
            PyEntries.objects.create(values[0],values[1],values[2],values[3],values[4])
        else:
            LhtEntries.objects.create(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8])
        
    def on_log(client, userdata, level, buf):
        print("log: ", buf)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_log = on_log
    client.username_pw_set(username, password)

    client.connect("eu1.cloud.thethings.network", 1883, 60)

    client.loop_start()
    client.subscribe("#") 
    time.sleep(1000)

    client.loop_stop()
    

# Create your views here.
def index(request):
    return HttpResponse("Hello World")
from .models import DeviceType
from .models import Device
from .models import PyEntries
from .models import LhtEntries

import paho.mqtt.client as mqtt
import time
import json

#function that takes a json format message and decodes it into dictionary value/pairs.
def returnMessage(message):
    message=message.decode()
    message="""{}""".format(message)
    '''
    json.load() takes a file object and returns the json object. It is contained in the json header.
    A JSON object contains data in the form of key/value pair. 
    The keys are strings and the values are the JSON types. 
    Keys and values are separated by a colon.
    '''
    mes=json.loads(message)
    print(mes["end_device_ids"]["device_id"])
    print(mes["uplink_message"]["decoded_payload"])
    #type conversion of the result of the json.loads() 'mes'.
    inp=dict(dev_id=mes["end_device_ids"]["device_id"])
    #sub json headers between the parameters given.
    inp["payload"]=mes["uplink_message"]["decoded_payload"]
    inp["time"]=mes["uplink_message"]["rx_metadata"][0]["time"]
    #return dictionary type of the result.
    return inp

def my_view( *args, **kwargs):
    
    # Iterate through all the data items
    # Add data to deviceType and Device for all available devices
    # Try catch/except statements to avoid error if a duplicate entry already exists. 
    # A pass statement is given meaning nothing should happen amd ignore the error.
    try:
        #directly referencing the fields to avoid error of entering in wrong field
        DeviceType.objects.create(type_id="py", type_name="pycom",attributes="battery powered, time, temperature, light, pressure")
    except:
        pass
    try:
        DeviceType.objects.create(type_id="lht", type_name="lhtcom",attributes="plugIn, time, temperature, light, Humidity, workmode, batteryVoltage")
    except:
        pass
    try:
        Device.objects.create(dev_uid="py-saxion", device_type=DeviceType.objects.get(type_id="py"), address="M.H. Tromplaan 28, 7513 AB, Enschede, Netherlands")
    except:
        pass
    try:
        Device.objects.create(dev_uid="py-wierden",device_type=DeviceType.objects.get(type_id="py") , address="Burgemeester J.C. van Den Bergplein 17-18, 7642 GS, Wierden")
    except:
        pass
    try:
        Device.objects.create(dev_uid="lht-gronau", device_type=DeviceType.objects.get(type_id="lht"), address="48599 Gronau, North Rhine-Westphalia, Germany")
    except:
        pass
    try:
        Device.objects.create(dev_uid="lht-wierden", device_type=DeviceType.objects.get(type_id="lht"), address="Burgemeester J.C. van Den Bergplein 17-18, 7642 GS, Wierden")
    except:
        pass
    try:
        Device.objects.create(dev_uid="lht-saxion", device_type=DeviceType.objects.get(type_id="lht"), address="M.H. Tromplaan 28, 7513 AB, Enschede, Netherlands")
    except:
        pass
    #call client method  to enter the actual data to the pyEntries and lhtEntries tables
    client()

#Method that connects to the MQTT server to fetch the data in json format
def client():
    #login required to connect to the server
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
        #retrieved msg json is decoded with the returnMessage() method defined above.
        values = returnMessage(msg.payload)
        #since the values is a dictionary type you can directly check values in keys
        # if dev_id contains 'py' then store data in the PyEntries table 
        if "py" in values["dev_id"]: 
            
            PyEntries.objects.create(
            #primary field has to directly reference that value
            dev_uid=Device.objects.get(dev_uid=values["dev_id"]), 
            entry_date=values["time"],
            light=values["payload"]["light"],
            temperature=values["payload"]["temperature"],
            pressure=values["payload"]["pressure"])
        #else store in the lhtEntries table.
        else:
            #try catch statement to deal with the difference of ILL_lx and TempC_DS values
            try:
                LhtEntries.objects.create(
                dev_uid=Device.objects.get(dev_uid=values["dev_id"]),
                entry_date=values["time"],
                BatV=values["payload"]["BatV"],
                Bat_status=values["payload"]["Bat_status"],
                Hum_SHT=values["payload"]["Hum_SHT"],
                ILL_lx=values["payload"]["ILL_lx"],
                TempC_SHT=values["payload"]["TempC_SHT"]
                )
            except:
                LhtEntries.objects.create(
                dev_uid=Device.objects.get(dev_uid=values["dev_id"]),
                entry_date=values["time"],
                BatV=values["payload"]["BatV"],
                Bat_status=values["payload"]["Bat_status"],
                Hum_SHT=values["payload"]["Hum_SHT"],
                TempC_DS=values["payload"]["TempC_DS"],
                TempC_SHT=values["payload"]["TempC_SHT"]
                )
            

            
    #debugging method to check if everything connected successfully
    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    #connect to the client to start collecting data
    client = mqtt.Client()
    #calls the on_connect and on_message defined above
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_log = on_log
    client.username_pw_set(username, password)
    #specify what MQTT is being used and the port number.
    client.connect("eu1.cloud.thethings.network", 1883, 60)
    print("Hello")
    try:
        #start looping and fetching data until a keyboard interrupt is made.
        client.loop_start()
        client.subscribe("#") 
        time.sleep(1000)
    except KeyboardInterrupt:
        client.loop_stop()



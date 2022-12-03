from .models import DeviceType
from .models import Device
from .models import PyEntries
from .models import LhtEntries

import paho.mqtt.client as mqtt
import time
import json


def returnMessage(message):
    message=message.decode()
    message="""{}""".format(message)
    mes=json.loads(message)
    print(mes["end_device_ids"]["device_id"])
    print(mes["uplink_message"]["decoded_payload"])
    inp=dict(dev_id=mes["end_device_ids"]["device_id"])
    inp["payload"]=mes["uplink_message"]["decoded_payload"]
    inp["time"]=mes["uplink_message"]["rx_metadata"][0]["time"]
    return inp

def my_view( *args, **kwargs):
    
    # Iterate through all the data items
    try:
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
        
        values = returnMessage(msg.payload)
        if "py" in values["dev_id"]: 
            
            PyEntries.objects.create(
            dev_uid=Device.objects.get(dev_uid=values["dev_id"]), 
            entry_date=values["time"],
            light=values["payload"]["light"],
            temperature=values["payload"]["temperature"],
            pressure=values["payload"]["pressure"])
            
        else:
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
            

            
        
    def on_log(client, userdata, level, buf):
        print("log: ", buf)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_log = on_log
    client.username_pw_set(username, password)

    client.connect("eu1.cloud.thethings.network", 1883, 60)
    print("Hello")
    try:
        client.loop_start()
        client.subscribe("#") 
        time.sleep(1000)
    except KeyboardInterrupt:
        client.loop_stop()



from .models import DeviceType
from .models import Device
from .models import PyEntries
from .models import LhtEntries
from datetime import date
from django.utils import timezone
from django.db import models
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
    #call client method  to enter the actual data to the pyEntries and lhtEntries tables
    client()
    client_g3()

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
            dev_uid=values["dev_id"], 
            entry_date=values["time"],
            light=values["payload"]["light"],
            temperature=values["payload"]["temperature"],
            pressure=values["payload"]["pressure"])
        #else store in the lhtEntries table.
        else:
            #try catch statement to deal with the difference of ILL_lx and TempC_DS values
            try:
                LhtEntries.objects.create(
                dev_uid=values["dev_id"],
                entry_date=values["time"],
                BatV=values["payload"]["BatV"],
                Bat_status=values["payload"]["Bat_status"],
                Hum_SHT=values["payload"]["Hum_SHT"],
                ILL_lx=values["payload"]["ILL_lx"],
                TempC_SHT=values["payload"]["TempC_SHT"]
                )
            except:
                LhtEntries.objects.create(
                dev_uid=values["dev_id"],
                entry_date=values["time"],
                BatV=values["payload"]["BatV"],
                Bat_status=values["payload"]["Bat_status"],
                Hum_SHT=values["payload"]["Hum_SHT"],
                TempC_DS=values["payload"]["TempC_DS"],
                TempC_SHT=values["payload"]["TempC_SHT"]
                )
        MetaData.objects.create9(
        entry_date=values["time"],
        dev_uid=values["dev_id"],
        BatV=values["payload"]["BatV"],
        Bat_status=values["payload"]["Bat_status"],
        gateway_uid=values["rx_metadata"]["gateway_ids"]["gateway_id"],
        rssi_val=values["rssi"],
        latitude=values["location"]["latitude"],
        longitude=values["location"]["longitude"],
        altitude=values["location"]["altitude"],
        bandwidth=values["bandwidth"],
        spreading_factor=values["spreading_factor"],
        frequency=values["frequency"],
        consumed_airtime=values["consumed_airtime"]
        )       
        get_values()
        
        

            

            
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

#Method that connects to the MQTT server to fetch the data in json format
def client_g3():
    #login required to connect to the server
    username = "saxion-weather-station-2@ttn"
    password = "NNSXS.G4XMJDI6W4BXH3Q6MXTBUOWDJ5GIUNKZJWGRMYQ.CBK6VE72OZR7UEAOPPU6HBW3E2742TZCHLSB5WCO7Z56D2FLPKWA"

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
            dev_uid=values["dev_id"], 
            entry_date=values["time"],
            light=values["payload"]["light"],
            temperature=values["payload"]["temperature"],
            pressure=values["payload"]["pressure"])
        #else store in the lhtEntries table.
        else:
            #try catch statement to deal with the difference of ILL_lx and TempC_DS values
            try:
                LhtEntries.objects.create(
                dev_uid=values["dev_id"],
                entry_date=values["time"],
                BatV=values["payload"]["BatV"],
                Bat_status=values["payload"]["Bat_status"],
                Hum_SHT=values["payload"]["Hum_SHT"],
                ILL_lx=values["payload"]["ILL_lx"],
                TempC_SHT=values["payload"]["TempC_SHT"]
                )
            except:
                LhtEntries.objects.create(
                dev_uid=values["dev_id"],
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

def get_values():
    start_date = datetime.today()
    end_date = datetime.today() - timedelta(days=1)
    global py_last_hour
    global lht_last_hour
    for x in range(23):
        py_last_day = PyEntries.objects.filter(entry_date__hour(x), entry_date__range=(start_date, end_date)).values('dev_uid').annotate(entry_date = x , avg_temp = Avg('temperature'), avg_pressure = Avg('pressure'), avg_light = Avg('light'), avg_batteryV = Avg('BatV'), avg_bat_status = Avg('Bat_status'))
        Py_Averages.objects.create(
        #primary field has to directly reference that value
        dev_uid=py_last_day["dev_id"], 
        entry_date=py_last_day["entry_date"],
        light=py_last_day["avg_light"],
        temperature=py_last_day["avd_temperature"],
        pressure=py_last_day["avg_pressure"]
        )
        lht_last_day = LhtEntries.objects.filter(entry_date__hour(x), entry_date__range=(start_date, end_date)).values('dev_uid').annotate(entry_date = x ,avg_humidity = Avg('Hum_SHT'), avg_light = Avg('ILL_lx'), avg_OutTemp = Avg('TempC_SHT'), avg_InTemp = Avg('TempC_DS'), avg_batteryV = Avg('BatV'), avg_bat_status = Avg('Bat_status'))
        try:
            Lht_Averages.objects.create(
            dev_uid=lht_last_day["dev_id"],
            entry_date=lht_last_day["entry_date"],
            BatV=lht_last_day["avg_batteryV"],
            Bat_status=lht_last_day["avg_bat_status"],
            Hum_SHT=lht_last_day["avg_humidity"],
            ILL_lx=lht_last_day["avg_light"],
            TempC_SHT=lht_last_day["avg_OutTemp"]
            )
        except:
            Lht_Averages.objects.create(
            dev_uid=lht_last_day["dev_id"],
            entry_date=lht_last_day["entry_date"],
            BatV=lht_last_day["avg_batteryV"],
            Bat_status=lht_last_day["avg_bat_status"],
            Hum_SHT=lht_last_day["avg_humidity"],
            TempC_DS=lht_last_day["avg_InTemp"],
            TempC_SHT=lht_last_day["avg_OutTemp"]
            )
    
    #meta data averages only done once a day at 12 miday
    currentDateAndTime = datetime.now()
    if  currentDateAndTime.hour == 12:
        meta_last_day = MetaData.objects.filter(entry_date__range=(start_date, end_date)).values('dev_uid','gateway_uid','latitude','latitude','altitude').annotate(avg_bat_v= Avg('BatV'),avg_bat_status = Avg('Bat_status'),avg_rssi = Avg('rssi_val'),avg_bandwidth = Avg('bandwidth'),avg_spreading_factor = Avg('spreading_factor'),avg_frequency = Avg('frequency'),avg_consumed_airtime = Avg('consumed_airtime'))
        MetaAvgs.objects.create(
        entry_date=datetime.now(),
        dev_uid=meta_last_day["dev_id"],
        BatV=meta_last_day["avg_bat_v"],
        Bat_status=meta_last_day["avg_bat_status"],
        gateway_uid=meta_last_day['avg_consumed_airtime'],
        rssi_val=meta_last_day["avg_rssi"],
        latitude=meta_last_day["location"],
        longitude=meta_last_day["location"],
        altitude=meta_last_day["location"],
        bandwidth=meta_last_day["avg_bandwidth"],
        spreading_factor=meta_last_day["avg_spreading_factor"],
        frequency=meta_last_day["avg_frequency"],
        consumed_airtime=meta_last_day["avg_consumed_airtime"]
        )       
    

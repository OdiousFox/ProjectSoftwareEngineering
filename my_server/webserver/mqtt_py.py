from .models import Meta_data
from .models import PyEntries
from .models import LhtEntries
from .models import Py_Averages
from .models import Lht_Averages
from django.db.models.functions import ExtractHour, ExtractMinute
from django.db.models import Avg, Value, Case, When
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
    inp["gate_id"]=mes["uplink_message"]["rx_metadata"][0]["gateway_ids"]['gateway_id']
    inp["long"]=mes["uplink_message"]["rx_metadata"][0]["location"]["longitude"]
    inp["lat"]=mes["uplink_message"]["rx_metadata"][0]["location"]["latitude"]
    
    inp["airtime"]=mes["uplink_message"]["consumed_airtime"].replace('s','')
    inp["rssi"]=mes["uplink_message"]["rx_metadata"][0]["rssi"]
    inp["snr"]=mes["uplink_message"]["rx_metadata"][0]["snr"]
    
    #return dictionary type of the result.
    return inp
## Calulate average value of payload
def updata_avg(id):
    res=None
    if "py" in id:
        res= PyEntries.objects.filter(dev_uid=id)\
        .annotate(hour=ExtractHour("entry_date"))\
            .values("hour","temperature","light","pressure","humidity")
    else:
        res=LhtEntries.objects.filter(dev_uid=id)\
            .annotate(hour=ExtractHour("entry_date"))\
                .values("hour","Bat_status","BatV","Hum_SHT","ILL_lx","TempC_DS","TempC_SHT")
    
    sto={}
    for i in range(24):
        sto[i]={"count":0}
        for key in res[0].keys():
            if key != "hour":
                if res[0][key] is not None:
                    sto[i][key]=0
                else:
                    sto[i][key]=None
    for val in res:
        sto[val["hour"]]["count"]+=1
        for key in val.keys():
            if key != "hour" :
                if val[key] is not None:
                    sto[val["hour"]][key]+=val[key]
                else:
                    sto[val["hour"]][key]=val[key]
    

    
    avg_sto={}
    for i in range(24):
        if sto[i]["count"]>0:
            avg_sto[i]={}
            for key in sto[i].keys():
                if key != "count" :
                    if(sto[i][key] is not None):
                        avg_sto[i][key]=sto[i][key]/sto[i]["count"]
                    else:
                        avg_sto[i][key]=None
   
    for i in avg_sto.keys():
        if "py" in id:
            que=Py_Averages.objects.filter(dev_uid=id,entry_hour=i)
            if(len(que)==0):
                Py_Averages.objects.create(
            #primary field has to directly reference that value
                dev_uid=id, 
                entry_hour=i,
                light=avg_sto[i]["light"],
                temperature=avg_sto[i]["temperature"],
                pressure=avg_sto[i]["pressure"],
                humidity=avg_sto[i]["humidity"])
            else:
                Py_Averages.objects.filter(dev_uid=id, entry_hour=i).update(
            #primary field has to directly reference that value
                light=avg_sto[i]["light"],
                temperature=avg_sto[i]["temperature"],
                pressure=avg_sto[i]["pressure"],
                humidity=avg_sto[i]["humidity"])
        else:
            que=Lht_Averages.objects.filter(dev_uid=id,entry_hour=i)
            if(len(que)==0):
                Lht_Averages.objects.create(
                    dev_uid=id,
                entry_hour=i,
                BatV=avg_sto[i]["BatV"],
                Bat_status=avg_sto[i]["Bat_status"],
                Hum_SHT=avg_sto[i]["Hum_SHT"],
                ILL_lx=avg_sto[i]["ILL_lx"],
                TempC_SHT=avg_sto[i]["TempC_SHT"],
                TempC_DS=avg_sto[i]["TempC_DS"]
                )
            else:
                Lht_Averages.objects.filter(dev_uid=id, entry_hour=i).update(
                BatV=avg_sto[i]["BatV"],
                Bat_status=avg_sto[i]["Bat_status"],
                Hum_SHT=avg_sto[i]["Hum_SHT"],
                ILL_lx=avg_sto[i]["ILL_lx"],
                TempC_SHT=avg_sto[i]["TempC_SHT"],
                TempC_DS=avg_sto[i]["TempC_DS"]
                )

        
    return 

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

        ## Store metadata
        try:
            Meta_data.objects.create(
            dev_uid = values["dev_id"],
            gateway_id = values["gate_id"],
            longitude = values["long"],    # Location longitude
            latitude = values["lat"],  # Location 
            rssi = values["rssi"],
            snr = values["snr"],
            airtime = values["airtime"]
            )
            updata_avg(values["dev_id"])
        except:
            print("Cannot update metadat for"+values["dev_id"])
        #get_values()
        
        

            

            
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
    
    #start looping and fetching data until a keyboard interrupt is made.
    client.loop_start()
    client.subscribe("#") 
       
    
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
        
            
        PyEntries.objects.create(
            #primary field has to directly reference that value
            dev_uid=values["dev_id"], 
            entry_date=values["time"],
            humidity=values["payload"]["humidity"],
            temperature=values["payload"]["temperature"],
            pressure=values["payload"]["pressure"])
        
        
        updata_avg(values["dev_id"])
        try:
            Meta_data.objects.create(
            dev_uid = values["dev_id"],
            gateway_id = values["gate_id"],
            longitude = values["long"],    # Location longitude
            latitude = values["lat"],  # Location 
            rssi = values["rssi"],
            snr = values["snr"],
            airtime = values["airtime"]
            )
            updata_avg(values["dev_id"])
        except:
            print("Cannot update metadat for"+values["dev_id"])
       
        
            

            
    #debugging method to check if everything connected successfully
    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    def calculate_Avgs():
        return



    #connect to the client to start collecting data
    client = mqtt.Client()
    #calls the on_connect and on_message defined above
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_log = on_log
    client.username_pw_set(username, password)
    #specify what MQTT is being used and the port number.
    client.connect("eu1.cloud.thethings.network", 1883, 60)
    print("Hello1")
   
    client.loop_start()
    client.subscribe("#") 
    return 
    

def get_values():
    global py_last_hour
    global lht_last_hour
    for x in range(23):
        py_last_day = PyEntries.objects.filter(entry_date_hour(x)).annotate(entry_date = x , avg_temp = Avg('temperature'), avg_pressure = Avg('pressure'), avg_light = Avg('light'), avg_batteryV = Avg('BatV'), avg_bat_status = Avg('Bat_status')).values()
        lht_last_day = LhtEntries.objects.filter(entry_date__hour(x)).annotate(entry_date = x ,avg_humidity = Avg('Hum_SHT'), avg_light = Avg('ILL_lx'), avg_OutTemp = Avg('TempC_SHT'), avg_InTemp = Avg('TempC_DS'), avg_batteryV = Avg('BatV'), avg_bat_status = Avg('Bat_status')).filter(entry_date__hour(x)).values()
    
    Py_Averages.objects.create(
    #primary field has to directly reference that value
    dev_uid=py_last_day["dev_id"], 
    entry_date=py_last_day["entry_date"],
    light=py_last_day["avg_light"],
    temperature=py_last_day["avd_temperature"],
    pressure=py_last_day["avg_pressure"]
    )

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

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db.models import Avg, Value, Case, When
from django.template import loader
from .models import Py_Averages
from .models import Lht_Averages
from .models import Meta_data
from .models import PyEntries
from .models import LhtEntries
from django.db.models.functions import ExtractHour
from datetime import timedelta
import re
import math
from threading import Thread
from . import mqtt_py
import json
import asyncio
## Documentaion for start_func() function
# @brief start listening data from sensor
def start_func(func):
    t=Thread(target=func)
    t.setDaemon=True
    t.start()
start_func(mqtt_py.client)
start_func(mqtt_py.client_g3)

#returns result in webformat
## Return the default website .
def init(request):
    tem=loader.get_template("index.html")
    return HttpResponse(tem.render())
## Documentaion for convertLux() function
# @brief Convert Lux (logarithmic scale) to linear scale(0 - 255)
def convertLux(lux):
    if(lux > 0):
        res=math.log10(lux)*(255/math.log10(65000))
        return res
    else:
        return 0
## Documentaion for formatMetadata(data) function
# @brief convert QuerySet type to Python type Dictionary from Metadata table
def formatMetadata(data):
    out = {}
    for key in data.keys():
        if key != "entry_id" and key != "dev_uid":
            out[key]=str(data[key])
    return out
## Documentaion for formatJson(data) function
# @brief convert QuerySet type to Python Dictionary type to be used to pass it to the website.
def formatJson(data):
    out={}
    for key in data[0].keys():
        if key != "entry_id" and key!= "dev_uid" and data[0][key] is not None:
            out[key]=[]
    for cont in data:
        for key in cont.keys():
            if key != "entry_id" and key!= "dev_uid" and cont[key] is not None:
                if key == "ILL_lx" :
                ## Convert Lux to percentage in linear scale 0 -> 255
                    if "light_intensity" not in out.keys():
                        out["light_intensity"]=[(convertLux(cont[key])/255)*100]
                    else:
                        out["light_intensity"].append((convertLux(cont[key])/255)*100)
                elif key =="light":
                    if "light_intensity" not in out.keys():
                        out["light_intensity"]=[cont[key]/255*100]
                    else:
                        out["light_intensity"].append(cont[key]/255*100)
                elif key == "temperature":
                    if "Inside_Temperature" not in out.keys():
                        out["Inside_Temperature"]=[cont[key]]
                    else:
                        out["Inside_Temperature"].append(cont[key])
                elif key == "TempC_SHT":
                    if cont["dev_uid"] == "lht-saxion":
                        if "Inside_Temperature" not in out.keys():
                            out["Inside_Temperature"]=[cont[key]]
                        else:
                            out["Inside_Temperature"].append(cont[key])
                    else:
                        if "Outside_Temperature" not in out.keys():
                            out["Outside_Temperature"]=[cont[key]]
                        else:
                            out["Outside_Temperature"].append(cont[key])

                elif key == "Hum_SHT" or key == "humidity":
                    if "Humidity" not in out.keys():
                        out["Humidity"]=[cont[key]]
                    else:
                        out["Humidity"].append(cont[key])
                elif key =="TempC_DS":
                    if "Outside_Temperature" not in out.keys():
                        out["Outside_Temperature"]=[cont[key]]
                    else:
                        out["Outside_Temperature"].append(cont[key])
                else:
                    out[key].append(cont[key])
    ## Remove empty key from the result
    empty_keys = [k for k in out if len(out[k])==0]
    for key in empty_keys:
        del out[key]            
    return out 
## Documentaion for spec_formatJson(inp) function
# @brief Return Python dictionary type for special request of json
def spec_formatJson(inp):
    res= formatJson(inp)
    prev_hour = None
    index = 0
    cur_hour = None
    hash_map={}
    ind = -1
    for index in range(0,len(res["hour"])):
        cur_hour=res["hour"][index]
        if cur_hour !=prev_hour:
            ind = ind + 1
            hash_map[ind]={}
            for key in res:
                hash_map[ind][key]=[]
            for key in res:
                hash_map[ind][key].append(res[key][index])
        else:
            for key in res:
                hash_map[ind][key].append(res[key][index])
        prev_hour = cur_hour
    out ={}
    for key in res:
        if key != "hour":
            out[key]=[]
   
    for ind_key in hash_map:
      
        for key in hash_map[ind_key]:
            if key != "entry_date" and key !="hour":
                out[key].append(sum(hash_map[ind_key][key])/len(hash_map[ind_key][key]))
            elif key == "entry_date":
                dt = hash_map[ind_key][key][0].replace(minute=0,second=0,microsecond=0)
               
                out[key].append(dt)
            else:
                continue
    
    return out
## Documentaion for default_api() function
# @brief Return Python dictionary which only has average values
def default_api():
    out ={}
    res=Lht_Averages.objects.values("dev_uid").distinct()
    for id in res:
        dev_id=id["dev_uid"]
        ndev_id=dev_id.replace("-","_")
        a=Lht_Averages.objects.filter(dev_uid=dev_id).order_by("entry_hour").values()
        if(len(a)==0):
            continue
        out[ndev_id]=formatJson(a)
        r=formatMetadata(Meta_data.objects.filter(dev_uid=dev_id).values().last())
        out[ndev_id]["meta_data"]=r
    res=Py_Averages.objects.values("dev_uid").distinct()
    for id in res:
        dev_id=id["dev_uid"]
        ndev_id=dev_id.replace("-","_")
        a=Py_Averages.objects.filter(dev_uid=dev_id).order_by("entry_hour").values()
        if(len(a)==0):
            continue
        out[ndev_id]=formatJson(a)
        r=formatMetadata(Meta_data.objects.filter(dev_uid=dev_id).values().last())
        out[ndev_id]["meta_data"]=r
    return out
## Documentation for spec_api() function
# @brief return specific Json api base on "Time-Period" header from API request
def spec_api(time):
    # @param time: Value of "Time-Period" header
    time=re.split('(\d+)',time)
    time=time[1:len(time)]
    out={}
    a = PyEntries.objects.values("dev_uid").distinct()
    for id in a:
        dev_id=id["dev_uid"]
        ndev_id=dev_id.replace("-","_")
        b = PyEntries.objects.filter(dev_uid=dev_id).values().last()
        earlier = b["entry_date"]-timedelta(days=int(time[0]), hours=int(time[2]))
       
        c = PyEntries.objects.filter(dev_uid=dev_id,entry_date__range=[earlier,b["entry_date"]])\
            .annotate(hour=ExtractHour("entry_date"))\
            .values()
        
        out[ndev_id]=spec_formatJson(c)
        out[ndev_id]["meta_data"]=formatMetadata(Meta_data.objects.filter(dev_uid=dev_id).values().last())
    a = LhtEntries.objects.values("dev_uid").distinct()
    for id in a:
        dev_id=id["dev_uid"]
        ndev_id=dev_id.replace("-","_")
        b = LhtEntries.objects.filter(dev_uid=dev_id).values().last()
       
        earlier = b["entry_date"]-timedelta(days=int(time[0]), hours=int(time[2]))
        
        c = LhtEntries.objects.filter(dev_uid=dev_id,entry_date__range=[earlier,b["entry_date"]])\
            .annotate(hour=ExtractHour("entry_date"))\
            .values()
       
        out[ndev_id]=spec_formatJson(c)
        out[ndev_id]["meta_data"]=formatMetadata(Meta_data.objects.filter(dev_uid=dev_id).values().last())
    #print(json.dumps(out, indent=4, sort_keys=True, default=str))
    return out
## Documentaion for fetch_api() function
# @brief fetches and returns the data on request depending on the request query.

def fetch_api(request):
    out = {}
    if("Time-period" not in request.headers ):
        out = default_api()
    elif(request.headers["Time-period"]=='default'):
        out = default_api()
    else:
        out= spec_api(request.headers["Time-period"])
    response=JsonResponse(out)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type, "
    response["Access-Control-Allow-Credentials"] = True
    return response

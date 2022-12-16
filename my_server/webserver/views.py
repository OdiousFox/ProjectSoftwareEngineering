
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from django.template import loader

from .models import DeviceType
from .models import Device
from .models import PyEntries
from .models import LhtEntries

from .mqtt_py import my_view


from threading import Thread
from . import mqtt_py

# Create your views here.
def start_func(func):
    t=Thread(target=func)
    t.setDaemon=True
    t.start()
start_func(mqtt_py.my_view)


#returns result in webformat
def init(request):
    tem=loader.get_template("index.html")
    return HttpResponse(tem.render())

#takes data from tables and returns it in json format to be used to pass it to the website.
def formatJson(data):
    out=dict()
    for container in data:
        for key in container:
            if key=="dev_uid_id":
                continue
            elif key!="entry_id":
                if container[key] is None:
                    continue
                if key not in out:
                    out[key]=[]
                d=container[key]
                if key=='entry_date':
                    #format the date in the format
                   d=d.strftime("%Y/%m/%d %H:%M:%S")
                out[key].append(d)
            else:
                continue
    #return the resulting json of data.
    return out
#fetches and returns the data on request depending on the request query.
def fetch_api(request):
    t1=PyEntries.objects.filter(dev_uid="py-wierden").values()
    t2=PyEntries.objects.filter(dev_uid="py-saxion").values()
    t3=LhtEntries.objects.filter(dev_uid="lht-saxion").values()
    t4=LhtEntries.objects.filter(dev_uid="lht-wierden").values()
    t5=LhtEntries.objects.filter(dev_uid="lht-gronau").values()
    dat1={}
    dat2={}
    dat3={}
    dat4={}
    dat5={}
    dat1["py_wierden"]=formatJson(t1)
    dat2["py_saxion"]=formatJson(t2)
    dat3["lht_saxion"]=formatJson(t3)
    dat4["lht_wierden"]=formatJson(t4)
    dat5["lht_gronau"]=formatJson(t5)
    merge={**dat1,**dat2,**dat3,**dat4,**dat5}
    #returns result in json.
    return JsonResponse(merge)


from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from django.template import loader

from .models import DeviceType
from .models import Device
from .models import PyEntries
from .models import LhtEntries

from .mqtt_py import my_view


from threading import Thread


# Create your views here.

def start(func,*args):
    t=Thread(target=func)
    
    t.start()
     
    return t
start(my_view)

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
    t1=PyEntries.objects.filter(dev_uid__contains = "py").values()
    t2=LhtEntries.objects.filter(dev_uid__contains = "lht").values()
    dat1={}
    dat2={}
    dat1["py_readings"]=formatJson(t1)
    dat2["lht_readings"]=formatJson(t2)
    merge={**dat1,**dat2}
    #returns result in json.
    return JsonResponse(merge)


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
     
    return
start(my_view)

def init(request):
    tem=loader.get_template("index.html")
    return HttpResponse(tem.render())
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
                   d=d.strftime("%Y/%m/%d %H:%M:%S")
                out[key].append(d)
            else:
                continue
    return out

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
    dat1["py-wierden"]=formatJson(t1)
    dat2["py-saxion"]=formatJson(t2)
    dat3["lht-saxion"]=formatJson(t3)
    dat4["lht-wierden"]=formatJson(t4)
    dat5["lht-gronau"]=formatJson(t5)
    merge={**dat1,**dat2,**dat3,**dat4,**dat5}
    
    return JsonResponse(merge)

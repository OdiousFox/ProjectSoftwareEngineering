from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.


def init(request):
    tem=loader.get_template("index.html")
    return HttpResponse(tem.render())
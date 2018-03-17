#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.


def index(request):
    List = ['渲染json', '到模板']
    Dict = {"site": "自强学堂", 'author': "uh3ng"}
    content = {'List': json.dumps(List),
               'Dict': json.dumps(Dict)
               }
    return render(request, 'home.html', content)


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


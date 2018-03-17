#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    string_val = 'this is content'
    li = [1, 2, 3, 4]
    cnt = map(str, range(100))
    return render(request, 'home.html', {'string': string_val, 'List': li, 'count': cnt})


def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a) + int(b)
    return HttpResponse(str(c))


def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


from django.shortcuts import render
from django.shortcuts import redirect
from login import models
# Create your views here.


def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if username and password:
            username = username.strip()
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return redirect('/index/')
                message = "密码不正确"
            except:
                message = "用户不存在"
        return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')


def register(request):
    return render(request, 'login/register.html')


def logout(request):
    return redirect("/index/")

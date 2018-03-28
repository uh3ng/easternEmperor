from django.shortcuts import render
from django.shortcuts import redirect
from login import models
from login import forms
# Create your views here.


def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写内容"
        # username = request.POST.get("username", None)
        # password = request.POST.get("password", None)
        # if username and password:
        #     username = username.strip()
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                message = "密码不正确"
            except:
                message = "用户不存在"
        return render(request, 'login/login.html', {
            'message': message
        })
    return render(request, 'login/login.html')


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写内容'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            gender = register_form.cleaned_data['gender']
            if password1 != password2:
                message = '两次输入密码不同'
                return render(request,
                              'login/register.html', locals())
            else:
                same_name = models.User.objects.filter(name=username)
                if same_name:
                    message = "用户已存在，请更换用户名"
                    return render(request,
                                  'login/register.html', locals())
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")

from django.shortcuts import render
from django.shortcuts import redirect
from login import models
from login import forms
import hashlib
# Create your views here.


def hash_code(s, salt="mysite"):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


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
                if user.password == hash_code(password):
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
                same_email = models.User.objects.filter(email=email)
                if same_email:
                    message = "邮箱已经注册过"
                    return render(request,
                                  'login/register.html', locals())

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.email = email
                new_user.gender = gender
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)

                message = '请立即前往邮箱， 进行邮件确认'
                return render(request, 'login/confirm.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def make_confirm_string(user):
    pass


def send_email(email, code):
    pass
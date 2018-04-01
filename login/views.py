from django.shortcuts import render
from django.shortcuts import redirect
from login import models
from login import forms
from django.conf import settings
import hashlib
import datetime
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
                if not user.has_confirmed:
                    message = "该用户还没有通过邮箱确认"
                    return render(request, 'login/login.html', locals())
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
                # send_email(email, code)

                message = '请立即前往邮箱， 进行邮件确认，没有收到邮件？'
                return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html')


def send_again(request):
    old_email = request.GET.get('email', None)
    new_email = request.POST.get('new_email', None)
    if new_email is None:
        return render(request, 'login/sendagain.html', locals())
    user = models.User.objects.filter(email=old_email)
    if user is None:
        message = '用户不存在'
    else:
        if user[0].has_confirmed:
            message = "你已经成功激活，不能修改邮箱！"
            return render(request, 'login/sendagain.html', locals())
        user[0].email = new_email
        user[0].save()
        code = models.ConfirmString.objects.get(user=user[0])
        send_email(new_email, code)
        message = '邮件已发送'
    return render(request, 'login/sendagain.html', locals())


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = "无效的确认请求"
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "邮件已经过期！请重新注册"
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "注册成功，欢迎登录"
        return render(request, 'login/confirm.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user,)
    return code


def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '注册确认邮件'
    text_content = """感谢注册www.uh3ng.com，这里是uh3ng的官方网站！\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！"""
    html_content = '''
    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.uh3ng.com</a>，\
                        这里是uh3ng的官方网站！</p>
                        <p>请点击站点链接完成注册确认！</p>
                        <p>此链接有效期为{}天！</p>
                        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
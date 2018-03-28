from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(max_length=128)
    password1 = forms.CharField(max_length=256)
    password2 = forms.CharField(max_length=256)
    email = forms.EmailField(max_length=128)
    gender = forms.ChoiceField(choices=gender)


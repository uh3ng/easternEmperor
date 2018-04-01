from django.urls import path
from login import views

app_name = 'login'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('confirm/', views.user_confirm, name="confirm"),
    path('sendagain/', views.send_again, name="sendagain"),
]
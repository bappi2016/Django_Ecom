from django.conf.urls import  url
from django.contrib import admin
from django.urls import path,re_path,include

from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    # path('login', views.Login.as_view(), name='login'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # url(r'^register/$', views.register_page, name='register'),
    # path('logout', views.LogoutView.as_view(), name='logout'),
]
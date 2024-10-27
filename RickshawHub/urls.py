
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from django.shortcuts import render
from .views import home,contact,viewProfile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('admin_module/', include('admin_module.urls')),
    path('driver/', include('driver.urls')),
    path('passenger/', include('passenger.urls')),
    path('contact/',contact,name='contact'),
    path('profile/',viewProfile,name='profile'),
]

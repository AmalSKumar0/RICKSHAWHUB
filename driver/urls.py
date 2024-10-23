from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('driver_login/', views.driver_login, name='driverLogin'),  
    path('driver_page/',views.driver_page, name='driverpage')
]
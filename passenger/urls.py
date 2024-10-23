from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('passenger_login/', views.passenger_login, name='passengerLogin'), 
    path('passenger_page/', views.passenger_page, name='passengerPage'), 
]
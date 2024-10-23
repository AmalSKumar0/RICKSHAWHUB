from django.urls import path
from django.shortcuts import render
from . import views
from .views import adminLog 


urlpatterns = [
    path('adminLog/', adminLog, name='adminLogin'),  
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  
]


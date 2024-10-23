
from django.contrib import admin
from django.urls import path,include
from django.http import HttpResponse
from django.shortcuts import render
from .views import home

def home(request):
    return render(request , 'homePage.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('admin_module/', include('admin_module.urls')),
    path('driver/', include('driver.urls')),
    path('passenger/', include('passenger.urls')),
]

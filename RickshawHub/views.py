from django.shortcuts import render
from passenger.models import Passenger
from driver.models import Driver

def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request,'contact.html')

def viewProfile(request):
    flag = request.session['whoami']
    if 'passenger_id' in request.session:
        passenger = Passenger.objects.get(pass_id = request.session['passenger_id'])
    else:
        passenger = Passenger.objects.none()
    if 'driver_id' in request.session:
        driver = Driver.objects.get(pass_id = request.session['driver_id'])
    else:
        driver = Driver.objects.none()
    
    return render(request,'profile.html',{
        'passenger':passenger,
        'driver':driver,
        'flag':flag,
    })
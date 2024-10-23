from django.shortcuts import render, redirect
from .forms import DriverLoginForm, DriverRegistrationForm, DriverLocForm
from .models import Driver, TemporaryDriver,Bookings
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.urls import reverse


def driver_page(request):
    flag = request.session.get('driverFlag', 1)
    
    if request.method == 'POST':
        driver_location = DriverLocForm(request.POST)
        if driver_location.is_valid():
            location = driver_location.cleaned_data['location']
            try:
                Driver.objects.filter(driver_id=request.session['driver_id']).update(current_location=location)
                request.session['driverFlag'] = 2
            except Driver.DoesNotExist:
                err = "User not found"
            return HttpResponseRedirect(reverse('driverpage'))
    else:
        driver_location = DriverLocForm()

    booking = Bookings.objects.filter(driver_id = request.session['driver_id'])

    driverdetails = Driver.objects.get(driver_id=request.session['driver_id'])
    return render(request, 'driver/driver.html', {
        'detail': driverdetails,
        'form': driver_location,
        'flag': flag,
        'booking':booking,
        })

def driver_login(request):
    err = ""
    if request.method == 'POST':
        # Login form processing
        form = DriverLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                # Check if the driver exists in the database
                driver = Driver.objects.get(email=email)
                
                # Use Django's check_password to verify the hashed password
                if check_password(password, driver.password):
                    request.session['driver_id'] = driver.driver_id  # Save driver ID in session
                    return redirect('driverpage')  # Redirect to the driver dashboard
                else:
                    err = "Incorrect password"
            except Driver.DoesNotExist:
                err = "User not found"

        # Registration form processing
        regForm = DriverRegistrationForm(request.POST, request.FILES)
        if regForm.is_valid():
            name = regForm.cleaned_data['name']
            email = regForm.cleaned_data['email']
            gender = regForm.cleaned_data['gender']
            address = regForm.cleaned_data['address']
            phone = regForm.cleaned_data['phone']
            licence = regForm.cleaned_data['licence']
            vehicle = regForm.cleaned_data['vehicle']
            image = regForm.cleaned_data['image']
            password = regForm.cleaned_data['password']

            # Hash the password before saving it
            hashed_password = make_password(password)

            # Save the new driver in the temporary driver table
            try:
                new_driver = TemporaryDriver(
                    name=name,
                    email=email,
                    gender=gender,
                    address=address,
                    phone=phone,
                    licence=licence,
                    vehicle=vehicle,
                    auto_img=image,
                    password=hashed_password  # Save the hashed password
                )
                new_driver.save()
                return redirect('success_page')  # Redirect to a success page
            except Exception as e:
                err = str(e)
        else:
            err = regForm.errors

    else:
        form = DriverLoginForm()  # Initialize login form
        regForm = DriverRegistrationForm()  # Initialize registration form

    return render(request, 'driver/DriverReg.html', {'form': form, 'regForm': regForm, 'err': err})

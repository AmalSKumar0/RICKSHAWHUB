from django.shortcuts import render, redirect
from .forms import DriverLoginForm, DriverRegistrationForm, DriverLocForm
from .models import Driver, TemporaryDriver,Bookings
from passenger.models import Passenger
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages




def driver_page(request):

    request.session['whoami']=2

    driverdetails = Driver.objects.get(driver_id=request.session['driver_id'])
    booking_det = Bookings.objects.filter(driver_id=request.session['driver_id'], status='accepted').first()
    
    # Determine the flag based on session or driver details
    if 'driverFlag' in request.session:
        flag = request.session['driverFlag']
    elif driverdetails.current_location is None:
        flag = request.session['driverFlag'] = 1
    elif not booking_det:
        flag = request.session['driverFlag'] = 2
    else:
        flag = request.session['driverFlag'] = 3

    # Actions based on GET parameters
    if 'goBack' in request.GET:
        request.session['driverFlag'] = 2
        return HttpResponseRedirect(reverse('driverpage'))

    if 'change' in request.GET:
        request.session['driverFlag'] = 1
        return HttpResponseRedirect(reverse('driverpage'))

    if 'offline' in request.GET:
        Driver.objects.filter(driver_id=request.session['driver_id']).update(current_location=None, is_live=False)
        request.session['driverFlag'] = 1
        request.session.flush()
        return render(request, 'index.html')

    # Accept booking
    if 'accept' in request.GET:
        passenger = request.GET['accept']
        try:
            Bookings.objects.filter(driver_id=request.session['driver_id'], pass_id=passenger).update(status='accepted')
            request.session['driverFlag'] = 3
            request.session['currentPass'] = passenger
        except Bookings.DoesNotExist:
            messages.error(request, 'Booking not found.')
        return HttpResponseRedirect(reverse('driverpage'))

    # Complete booking
    if 'completed' in request.GET:
        otp = request.GET.get('otp')
        try:
            otp_real = Bookings.objects.get(driver_id=request.session['driver_id'], status='accepted', OTP=otp)
            Bookings.objects.filter(driver_id=request.session['driver_id'], OTP=otp).update(status='completed')
            request.session['driverFlag'] = 4
        except Bookings.DoesNotExist:
            messages.error(request, 'Invalid OTP or booking not found.')
        return HttpResponseRedirect(reverse('driverpage'))

    # Cancel booking
    if 'cancel' in request.GET:
        passenger = request.GET['cancel']
        try:
            Bookings.objects.filter(driver_id=request.session['driver_id'], pass_id=passenger).update(status='canceled')
            request.session['driverFlag'] = 2
        except Bookings.DoesNotExist:
            messages.error(request, 'Booking not found.')
        return HttpResponseRedirect(reverse('driverpage'))

    # Update location if POST request
    if request.method == 'POST':
        driver_location = DriverLocForm(request.POST)
        if driver_location.is_valid():
            location = driver_location.cleaned_data['location']
            try:
                Driver.objects.filter(driver_id=request.session['driver_id']).update(current_location=location)
                request.session['driverFlag'] = 2
            except Driver.DoesNotExist:
                messages.error(request, "Driver not found.")
            return HttpResponseRedirect(reverse('driverpage'))
    else:
        driver_location = DriverLocForm()

    # Retrieve current passenger and booking if available
    current_passenger = Passenger.objects.filter(pass_id=request.session.get('currentPass')).first()
    current_request = Bookings.objects.filter(driver_id=request.session['driver_id'], pass_id=request.session.get('currentPass')).first()

    # Other necessary data
    booking = Bookings.objects.filter(driver_id=request.session['driver_id'], status='requested')
    Driver_from = driverdetails.current_location
    price = Bookings.objects.filter(driver_id=request.session['driver_id']).exclude(status='requested').values_list('price', flat=True).first()

    return render(request, 'driver/driver.html', {
        'detail': driverdetails,
        'form': driver_location,
        'flag': flag,
        'booking': booking,
        'cur_pass': current_passenger,
        'cur_book': current_request,
        'price': price,
        'from': Driver_from,
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

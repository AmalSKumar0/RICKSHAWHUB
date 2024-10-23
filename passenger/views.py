from django.shortcuts import render,redirect
from .forms import PassengerLoginForm,PassengerRegistrationForm,searchAuto
from .models import Passenger
from driver.models import Driver,Bookings,CompletedBookings,Reviews
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from.utils import get_distance_between_places,generate_otp,calculate_trip_price


def passenger_page(request):
    flag = request.session.get('passengerFlag', 1)

    # if passenger click another location button
    if request.GET.get('another_location') == 'true':
        request.session['passengerFlag'] = 1
        return HttpResponseRedirect(reverse('passengerPage'))
    
    # if passenger tries to pay for the auto
    if 'payment' in request.GET:
        request.session['lookedupdriver'] = request.GET['payment']
        request.session['paymentwindow'] = True
        return HttpResponseRedirect(reverse('passengerPage'))
    
    # if he dont want to pay and return to view other auto
    if 'Back' in request.GET:
        request.session['paymentwindow'] = False
        return HttpResponseRedirect(reverse('passengerPage'))
    
    # if passenger pays and book the auto
    if 'BookDriver' in request.GET:
        bookings = Bookings(
            pass_id = request.session['passenger_id'],
            driver_id = request.GET['BookDriver'],
            from_location = request.session['from'],
            to_location = request.session['to'],
            landmark = request.session['landmark'],
            status = 'requested',
            distance = request.session['distance'],
            price = request.session['price'],
            OTP = generate_otp()
        )
        bookings.save()
        request.session['bookingID']=bookings.book_id
        request.session['paymentwindow'] = False
        request.session['passengerFlag'] = 3
        return redirect('passengerPage')

    # fetching data from bookings
    if 'bookingID' in request.session:
        booking = Bookings.objects.get(book_id=request.session['bookingID'])
    else:
        booking = Bookings.objects.none()

    # fetching data of thr viewd and booked driver
    if 'lookedupdriver' in request.session:
        lookedupdriver = Driver.objects.get(driver_id = request.session['lookedupdriver'])
    else:
        lookedupdriver = Driver.objects.none()
    
    # getting passenger details
    passenger = Passenger.objects.get(pass_id=request.session['passenger_id'])
    available_drivers = Driver.objects.none()

    # Retrieve any errors from the session, if available
    paymentwindow = request.session.get('paymentwindow', False)
    err = request.session.get('err', '')
    error = request.session.get('error', '')
    distance = request.session.get('distance',0)
    price = request.session.get('price',0)

    if request.method == 'POST':
    
        searchForm = searchAuto(request.POST)
        
        if searchForm.is_valid():
            fromLoc = searchForm.cleaned_data['from_loc']
            toLoc = searchForm.cleaned_data['to_loc']
            landmark = searchForm.cleaned_data['landmark']
            request.session['distance']=get_distance_between_places(fromLoc,toLoc)
            request.session['price']=calculate_trip_price(request.session['distance'])

            # Store search data in session
            request.session['from'] = fromLoc
            request.session['to'] = toLoc
            request.session['landmark'] = landmark
            
            try:
                # Attempt to find drivers in the specified location
                available_drivers = Driver.objects.filter(current_location=fromLoc).exclude(Q(bookings__status__isnull=False) & ~Q(bookings__status="requested"))
                request.session['error'] = str(available_drivers)
                
                # If drivers are found, store their IDs in session
                if available_drivers.exists():
                    request.session['available_driver_ids'] = list(available_drivers.values_list('driver_id', flat=True))
                    request.session['passengerFlag'] = 2
                else:
                    # No drivers found; update flag accordingly
                    request.session['passengerFlag'] = 2

                return redirect('passengerPage')

            except Driver.DoesNotExist:
                # No driver found in the given location, handle gracefully
                request.session['err'] = "No drivers available at the selected location."
                request.session['passengerFlag'] = 2  # Set flag for "no drivers"
                return redirect('passengerPage')

            except Exception as e:
                # Log the actual exception and set error flag
                request.session['err'] = str(e)  # Save the exception as a string
                request.session['passengerFlag'] = 4  # Set flag for error
                print(f"Error during driver search: {e}")  # Debugging: Print the error
                return redirect('passengerPage')
    else:
        searchForm = searchAuto()

    # Load available drivers from session if any
    if 'available_driver_ids' in request.session:
        driver_ids = request.session['available_driver_ids']
        available_drivers = Driver.objects.filter(driver_id__in=driver_ids)
    
    # Process location if set in session
    from_location = request.session.get('from', '').split()[0].strip(',')
    to_location = request.session.get('to', '').split()[0].strip(',')

    return render(request, 'passenger/passenger.html', {
        'passenger_details': passenger,
        'flag': flag,
        'searchForm': searchForm,
        'driverInLocation': available_drivers,
        'from': from_location,
        'to': to_location,
        'err': err,
        'error':error,
        'paymentwindow':paymentwindow,
        'distance':distance,
        'price':price,
        'lookedupdriver':lookedupdriver,
        'booking':booking,

    })

def passenger_login(request):
    err = ''
    if request.method == 'POST':
        login_form = PassengerLoginForm(request.POST)
        register_form = PassengerRegistrationForm(request.POST)

        if login_form.is_valid():  # Check login form validity
            email = login_form.cleaned_data['email_id']
            password = login_form.cleaned_data['password']
            try:
                passenger = Passenger.objects.get(email=email)
                if passenger.password == password:
                    request.session['passenger_id'] = passenger.pass_id
                    return redirect('passengerPage')
                else:
                    err = "Incorrect password"
            except Passenger.DoesNotExist:
                err = "User not found"
        
        # Check registration form validity
        elif register_form.is_valid():
            name = register_form.cleaned_data['name']
            email = register_form.cleaned_data['email']
            gender = register_form.cleaned_data['gender']
            address = register_form.cleaned_data['address']
            phone_no = register_form.cleaned_data['phone']
            password = register_form.cleaned_data['password']
            try:
                new_passenger = Passenger(
                    name=name,
                    email=email,
                    gender=gender,
                    address=address,
                    phone_no=phone_no,
                    password=password
                )
                new_passenger.save()
                passenger = Passenger.objects.get(email=email)
                request.session['passenger_id']=passenger.pass_id
                return redirect('passengerPage')  # Redirect to a success page
            except Exception as e:
                err = str(e)
    else:
        login_form = PassengerLoginForm()
        register_form = PassengerRegistrationForm()

    return render(request, 'passenger/PassReg.html', {'RegisterForm': register_form, 'LoginForm': login_form, 'err': err})

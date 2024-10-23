from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminTable
from driver.models import Driver,TemporaryDriver,Bookings,CompletedBookings
from passenger.models import Passenger
from .forms import AdminLoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse



def adminLog(request):
    err = ""
    form = AdminLoginForm()
    if request.method == 'POST':
        print('Form is submitted')  # Debug: Check if form is submitted
        form = AdminLoginForm(request.POST)

        print(f'Form Data: {request.POST}')  # Debug: Print the submitted form data

        if form.is_valid():
            print('Form is valid')  # Debug: Check if the form is valid
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            print(f'Email: {email}, Password: {password}')  # Debug: Show cleaned data

            try:
                admin_user = AdminTable.objects.get(email=email)
                print(f'Admin User Found: {admin_user}')  # Debug: Print found user

                if admin_user.password == password:
                    print("Login successful!")  # Debug: Print login success message
                    request.session['admin'] = admin_user.name  # Save admin name in session
                    return redirect('admin_dashboard')  # Redirect to admin dashboard
                else:
                    err = "Incorrect password"
                    print(err)  # Debug: Password mismatch
            except AdminTable.DoesNotExist:
                err = "User not found"
                print(err)  # Debug: User does not exist
        else:
            print('Form is not valid')  # Debug: Form is not valid
            print(form.errors)  # Debug: Show form errors
    else:
        form = AdminLoginForm()
    return render(request, 'admin_module/adminLog.html',{'form': form, 'err': err})


def admin_dashboard(request):
    flag = request.session.get('adminFlag', 1)

    if request.GET.get('accept'):
        accepteddriver = TemporaryDriver.objects.get(driver_id=request.GET.get('accept'))
        newdriver = Driver(
            name = accepteddriver.name,
            email = accepteddriver.email,
            phone = accepteddriver.phone,
            address = accepteddriver.address,
            vehicle = accepteddriver.vehicle,
            licence = accepteddriver.licence,
            password = accepteddriver.password,
            gender = accepteddriver.gender,
            auto_img = accepteddriver.auto_img,
            created_at = accepteddriver.created_at
        )
        newdriver.save()
        accepteddriver.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))
        
    if request.GET.get('deleteNewDriver'):
        deleteddriver =TemporaryDriver.objects.get(driver_id=request.GET.get('deleteNewDriver'))
        deleteddriver.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))
    
    if request.GET.get('deleteDriver'):
        deleteddriver =Driver.objects.get(driver_id=request.GET.get('deleteDriver'))
        deleteddriver.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))
    
    if request.GET.get('deleteBooking'):
        deletedbooking = Bookings.objects.get(book_id=request.GET.get('deleteBooking'))
        deletedbooking.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))
    
    if request.GET.get('deletePassenger'):
        deletedPassenger = Passenger.objects.get(pass_id=request.GET.get('deletePassenger'))
        deletedPassenger.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))

    # Check GET parameters to update the session flag
    if request.GET.get('newDrivers') == 'true':
        request.session['adminFlag'] = 1
        return HttpResponseRedirect(reverse('admin_dashboard'))  # Redirect to same page after updating

    elif request.GET.get('allPassengers') == 'true':
        request.session['adminFlag'] = 2
        return HttpResponseRedirect(reverse('admin_dashboard'))

    elif request.GET.get('allDrivers') == 'true':
        request.session['adminFlag'] = 3
        return HttpResponseRedirect(reverse('admin_dashboard'))

    elif request.GET.get('bookings') == 'true':
        request.session['adminFlag'] = 4
        return HttpResponseRedirect(reverse('admin_dashboard'))

    # Render the template with 'admin_name' and 'flag'
    drivers = Driver.objects.all()
    passengers = Passenger.objects.all()
    bookings = Bookings.objects.all()
    newdrivers = TemporaryDriver.objects.all()
    return render(request, 'admin_module/admin.html', {
        'admin_name': request.session.get('admin', 'Admin'),
        'adminFlag': flag,
        'drivers': drivers,
        'passengers' : passengers,
        'bookings' : bookings,
        'newdrivers' : newdrivers,
    })

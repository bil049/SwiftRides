from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import uuid, json, paystack
from django.conf import settings
from django.http import JsonResponse
from paystackapi.transaction import Transaction as PaystackTransaction
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from swiftrides_companies.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.crypto import get_random_string
from django.db.models import Q


def userlogin(request):
    form = CreateUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                account = Account.objects.get(user=user)
                return redirect('index')  # Redirect to dashboard if profile exists
            except Account.DoesNotExist:
                messages.success(request, user + ' is logged in, fill form to complete registration')
                return redirect('userregistration')  # Redirect to registration if profile doesn't exist
        else:
            messages.error(request, 'Invalid username or password')
    context = {'form': form}
    return render(request, 'swiftrides/login.html', context)
# Create your views here.

def userregister (request): 
    form = CreateUserForm()
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            user = form.cleaned_data.get('username')
            messages.success(request, 'User created successfully for ' + user)
            return HttpResponseRedirect(reverse('userlogin'))
        else:
            error_message = ""
            for field, errors in form.errors.items():
                for error in errors:
                    error_message += f"{field}: {error}\n"
            messages.error(request, error_message)
    context_dictionary = {'form': form}
    return render(request, 'swiftrides/register.html', context_dictionary)

def userregistration (request):
    form = AccountForm(user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(commit=True)
            name = form.cleaned_data.get('fullname')
            messages.success(request, 'Registration completed for ' + name)
            return redirect('index')
    else:
        form = AccountForm(user=request.user)    
    context={'form' : form}
    return render (request, 'swiftrides/completeregistration.html', context)

def index(request):
    profiles = Profile.objects.all()
    user_account = Account.objects.get(user=request.user)
    cars = Car.objects.filter(is_available=True)
    context = {
        'profiles': profiles,
        'account': user_account,
        'cars': cars
    }
    return render(request, 'swiftrides/index.html', context)

def rentalcompanies(request):
    profiles = Profile.objects.all()
    user_account = Account.objects.get(user=request.user)
    context = {
        'profiles': profiles,
        'account': user_account,
    }
    return render(request, 'swiftrides/rentalcompanies.html', context)

def logoutUser(request):
    logout(request)
    return redirect(userlogin)

@login_required
def updateaccount(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance =account, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('userdashboard')
    else:
        form = AccountForm(instance=account, user=request.user)
    return render(request, 'swiftrides/completeregistration.html',  {'form': form, 'account': account})

@login_required
def updatereservation(request,pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance =reservation, user=request.user)
        if form.is_valid():
            form.save()
            
            return redirect('userdashboard')
    else:
        form = ReservationForm(instance=reservation, user=request.user)
    return render(request, 'swiftrides/rentcar.html',  {'form': form, 'reservation': reservation})

@login_required
def company_cars(request, company_name):
    # Retrieve cars posted by the rental company with the specified company_name
    cars = Car.objects.filter(user__profile__company_name=company_name)


    user_profile = Profile.objects.get(company_name=company_name)
    

    # Retrieve cars associated with the current user
    
    user_cars = Car.objects.filter( user__profile__company_name=company_name, is_available=True)

    context = {
        "user_cars": user_cars,
        "user_profile": user_profile,
        "company_name": company_name,
        "cars": cars
    }
    
    return render(request, 'swiftrides/cars.html', context)

@login_required
def available_cars(request):
    # Retrieve cars posted by the rental company with the specified company_name
    available_cars = Car.objects.filter(is_available=True)

    context = {
        "available_cars": available_cars
    }
    
    return render(request, 'swiftrides/availablecars.html', context)

@login_required
def singlecar(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'swiftrides/singlecar.html', {'car': car})

@login_required
def rentcar(request, car_id, company_name):
    car = get_object_or_404(Car, pk=car_id)
    form = ReservationForm(user=request.user)
    user_profile = Profile.objects.get(company_name=company_name)
    if request.method == 'POST':
        form= ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.car_id = car_id
            reservation.save()
            # Redirect to payment page with reservation details
            redirect_url = reverse('initiatepayment') + f'?reservation_id={reservation.id}'
            return redirect(redirect_url)            
                 
        else:
            print(form.errors)
            
    else:
        form = ReservationForm(user=request.user, initial={'car': car_id})
    return render(request, 'swiftrides/rentcar.html', {'car': car,'form': form, 'user_profile': user_profile, 'company_name': company_name})

@login_required
def userdashboard(request):
    user_account = Account.objects.get(user=request.user)
    current_reservations = Reservation.objects.filter(
        user=request.user,
        dropoff__gte=timezone.now()  # Filter reservations where drop-off date is in the future
    )
    
    # Get all reservations for the logged-in user
    all_reservations = Reservation.objects.filter(user=request.user)
    
    context = {
        'account': user_account,
        'current_reservations': current_reservations,
        'all_reservations': all_reservations,
    }
    return render(request, 'swiftrides/userdashboard.html', context)

@login_required
def cancelreservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
   
    reservation.delete()
    messages.success(request, 'Reservation canceled successfully.')
    return redirect(userdashboard) 
    

@login_required
def initiate_payment(request: HttpRequest) -> HttpResponse:
    reservation_id = request.GET.get('reservation_id')
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    email = request.user.email
    amount = reservation.car.price  

    days = (reservation.dropoff - reservation.pickup).days
    if days < 1:
        days = 1  

    
    daily_price = int(reservation.car.price)  
    total_amount = daily_price * days

    if request.method == "POST":
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.user = request.user  
            payment.reservation = reservation
            payment.save()
            return render(request, 'swiftrides/makepayment.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        initial_data = {'email': email, 'amount': total_amount}
        payment_form = PaymentForm(initial=initial_data)

    return render(request, 'swiftrides/initiatepayment.html', {'payment_form': payment_form, 'reservation': reservation})


@login_required
def verify_payment(request: HttpRequest, reference: str) -> HttpResponse:
    payment = get_object_or_404(Payment, reference=reference)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Verification successful')
    else:
        messages.error(request, 'Verification failed')
        return redirect('initiatepayment')
    return redirect('userdashboard')

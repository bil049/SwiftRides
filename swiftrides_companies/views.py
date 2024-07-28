from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def register (request): 
    form = CreateUserForm()
    if request.method == 'POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            user = form.cleaned_data.get('username')
            messages.success(request, 'User created successfully for ' + user)
            return HttpResponseRedirect(reverse('login'))
        else:
            error_message = ""
            for field, errors in form.errors.items():
                for error in errors:
                    error_message += f"{field}: {error}\n"
            messages.error(request, error_message)
    context_dictionary = {'form': form}
    return render(request, 'swiftridescompany/companyregister.html', context_dictionary)

def registration (request):
    form = ProfileForm(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(commit=True)
            name = form.cleaned_data.get('company_name')
            messages.success(request, 'Registration completed for ' + name)
            return redirect('dashboard')
    else:
        form = ProfileForm(user=request.user)    
    context={'form' : form}
    return render (request, 'swiftridescompany/completeregistration.html', context)


def loginPage(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                profile = Profile.objects.get(user=user)
                return redirect('dashboard')  # Redirect to dashboard if profile exists
            except Profile.DoesNotExist:
                messages.success(request, 'Logged in, fill form to complete registration')
                return redirect('registration')  # Redirect to registration if profile doesn't exist
        else:
            messages.error(request, 'Invalid username or password')
    context = {'form': form}
    return render(request, 'swiftridescompany/companylogin.html', context)



def logoutUser(request):
    logout(request)
    return redirect(loginPage)

@login_required
def companycar(request):
    context_dictionary = {
        "user_cars" : Car.objects.filter(user=request.user),
        "user_profile" : Profile.objects.get(user=request.user)
    }
    
    return render(request, 'swiftridescompany/companycars.html', context_dictionary )

def dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'swiftridescompany/dashboard.html', {'profile': user_profile})

@login_required
def rentedcars(request):
    context_dictionary = {
        "user_cars" : Car.objects.filter(user=request.user, is_available=False),
        "user_profile" : Profile.objects.get(user=request.user)
    }
    
    return render(request, 'swiftridescompany/rentedcars.html', context_dictionary )

def dashboard(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'swiftridescompany/dashboard.html', {'profile': user_profile})

@login_required
def uploadcar(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car uploaded')
            return redirect('companycar')
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)
    
    else:
        form = CarForm(user=request.user)

    context = {'form': form}
    return render(request, 'swiftridescompany/uploadcar.html', context)

@login_required
def details(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'swiftridescompany/cardetails.html', {'car': car})

@login_required
def update_cardetails(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('cardetails', car_id=pk)
    else:
        form = CarForm(instance=car)
    return render(request, 'swiftridescompany/uploadcar.html', {'form': form, 'car': car})

@login_required
def updateprofile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance =profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'swiftridescompany/completeregistration.html',  {'form': form, 'profile': profile})
    

@login_required
def delete_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    car.delete()
    messages.success(request, 'Car deleted')
    return redirect('companycar')
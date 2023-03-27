from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Store, Address


# Create your views here.
def home(request):
    return render(request, 'Main/Login/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'Main/Login/login.html')


def register(request):
    if request.method == 'POST':
        # PERSONAL USER INFO
        username = request.POST['userName']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        customer_address = request.POST['cusAddr']

        # STORE INFO
        store_name = request.POST['storeName']
        store_address = request.POST['storeAddress']
        email = request.POST['emailAddr']

        # LOGIN INFO
        password = request.POST['password']
        confirm = request.POST['confirmPass']
        image = request.POST['formFile']

        if password != confirm:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'Passwords do not match.'
            })

        try:
            newUser = User(username=username, first_name=first_name, last_name=last_name,
                           password=password, email=email)

            new_address = Address(address_name=customer_address, user=newUser)
            new_store = Store(storeName=store_name, storeOwner=newUser, storeAddress=store_address)

            newUser.save()
            new_address.save()
            new_store.save()

        except IntegrityError:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'User already exists.'
            })

        login(request, newUser)
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'Main/Login/register.html')


## VIEWS FOR LOGGED IN USERS

def dashboard(request):
    user = request.user
    return render(request, 'Main/Landing/dashboard.html', {
        'user': user
    })


def inventory(request):
    user = request.user

    return render(request, 'Main/Landing/inventory.html', {
        'user': user
    })


def accounting(request):
    user = request.user

    return render(request, 'Main/Landing/accounting.html', {
        'user': user
    })


def profile(request):
    user = request.user

    return render(request, 'Main/Landing/profile.html', {
        'user': user
    })


def help(request):
    user = request.user

    return render(request, 'Main/Landing/help.html', {
        'user': user
    })


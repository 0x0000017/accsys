import sys
import pandas as pd
sys.path.append('..')

from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Store, Address, Item, Sale


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
        username = request.POST['username']
        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        customer_address = request.POST['address']

        # STORE INFO
        store_name = request.POST['storeName']
        store_address = request.POST['storeAddress']
        email = request.POST['email']

        # LOGIN INFO
        password = request.POST['password']
        confirm = request.POST['confirmPass']

        if password != confirm:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'Passwords do not match.'
            })

        try:
            newUser = User(username=username, first_name=first_name, last_name=last_name,
                           password=password, email=email)

            new_address = Address(address_name=customer_address, user=newUser)

            new_store = Store(storeName=store_name, storeAddress=store_address)
            newUser.save()
            new_address.save()
            new_store.save()

            new_store.storeOwner.add(newUser)
            new_store.save()

        except IntegrityError:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'User already exists.'
            })

        login(request, newUser)
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'Main/Login/register.html')


# VIEWS FOR LOGGED IN USERS
def dashboard(request):
    user = request.user
    return render(request, 'Main/Landing/dashboard.html', {
        'user': user
    })


def inventory(request, item_filter):
    user = request.user
    item_set = item_filter.lower()

    if item_set == 'all':
        items = Item.objects.all()[:201]
    elif item_set == 'name':
        items = Item.objects.order_by('item_name').all()[:201]
    elif item_set == 'price':
        items = Item.objects.order_by('item_price').all()[:201]
    elif item_set == 'category':
        items = Item.objects.order_by('category').all()[:201]
    elif item_set == 'date':
        items = Item.objects.order_by('date_ordered').all()[:201]
    elif item_set == 'quantity':
        items = Item.objects.all()[:201]

    return render(request, 'Main/Landing/inventory.html', {
        'user': user,
        'items': items
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


def profit(request):
    user = request.user

    return render(request, 'Main/Landing/profit.html', {
        'user': user
    })


def sales(request):
    user = request.user

    return render(request, 'Main/Landing/sales.html', {
        'user': user
    })


def expenses(request):
    user = request.user

    return render(request, 'Main/Landing/expenses.html', {
        'user': user
    })


def generate_data(request):
    df = pd.read_csv('Main/datasets/Processed Superstore Data.csv')
    store = Store.objects.get(id=1)

    for i in range(2, len(df.index)):
        new_item = Item(item_name=df['Sub-Category'][i],
                        item_price=df['Price per Item'][i],
                        category=df['Category'][i],
                        store=store)
        new_item.save()

    return HttpResponse('Generation Complete')


def generate_sale_data(request):
    df = pd.read_csv('Main/datasets/Processed Superstore Data.csv')
    items = Item.objects.all()
    store = Store.objects.get(id=1)

    for i in range(2, len(df.index)):
        new_sale = Sale(item_name=df['Sub-Category'][i],
                        item_price=df['Price per Item'][i],
                        category=df['Category'][i],
                        store=store)
        new_sale.save()

    return HttpResponse('Generation Complete')


def delete_data(request):
    items = Item.objects.all()
    items.delete()

    return HttpResponse('Items Deleted')
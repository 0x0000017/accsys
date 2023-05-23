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
    store = Store.objects.filter(storeOwner=user)
    items = Item.objects.filter(store__in=store).all()
    total_expenses = 1
    total_sales = 1
    revenue = 1
    net_income = 1
    office_sales = check_top_sales(items)[0]
    furniture_sales = check_top_sales(items)[1]
    tech_sales = check_top_sales(items)[2]

    # for item in items:
    #     total_expenses += item.expense

    return render(request, 'Main/Landing/dashboard.html', {
        'user': user,
        'sales': total_sales,
        'revenue': revenue,
        'expense': total_expenses,
        'net_income': net_income,
        'all_items': items,
        'recent_sales': Item.objects.filter(store__in=store).all()[:10:-1],
        'office_sales': office_sales,
        'furniture_sales': furniture_sales,
        'tech_sales': tech_sales,
    })


def inventory(request, item_filter):
    user = request.user
    store = Store.objects.filter(storeOwner=user)
    item_set = item_filter.lower()

    if item_set == 'all':
        items = Item.objects.filter(store__in=store).all()
    else:
        items = Item.objects.filter(store__in=store).order_by(f'{item_set}').all()

    return render(request, 'Main/Landing/inventory.html', {
        'user': user,
        'all_items': items,
        'items': items[:round(len(items) * .2)]
    })


def accounting(request, filter_data):
    user = request.user

    return render(request, 'Main/Landing/accounting.html', {
        'user': user,
        'panel': filter_data.capitalize()
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


def generate_data(request):
    df = pd.read_csv('Main/datasets/Processed Superstore Data.csv')
    store = Store.objects.get(id=1)

    for i in range(2, len(df.index)):
        new_item = Item(item_name=df['Sub-Category'][i],
                        item_price=df['Price per Item'][i],
                        expense=df['Production Cost'][i],
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


def check_top_sales(items):
    categs = [0, 0, 0]

    for item in items:
        if item.category == 'Office Supplies':
            categs[0] += 1
        elif item.category == 'Furniture':
            categs[1] += 1
        elif item.category == 'Technology':
            categs[2] += 1

    return categs
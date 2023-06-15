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
from datetime import datetime
import random


# Create your views here.
def home(request):
    return render(request, 'Main/Login/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'Main/Login/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


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
            newUser = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
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
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    store = Store.objects.filter(storeOwner=user)
    items = Item.objects.filter(store__in=store).all()
    total_expenses = 0
    revenue = 0
    office_sales = check_top_sales(items)[0]
    furniture_sales = check_top_sales(items)[1]
    tech_sales = check_top_sales(items)[2]
    total_sales = 0

    for item in items:
        total_expenses += item.expense
        revenue += item.item_price

    for sale in Sale.objects.filter(store__in=store):
        total_sales += sale.amount

    net_income = revenue - total_expenses

    return render(request, 'Main/Landing/dashboard.html', {
        'user': user,
        'sales': total_sales,
        'revenue': revenue,
        'expense': total_expenses,
        'net_income': net_income,
        'all_items': items,
        'recent_sales': Sale.objects.filter(store__in=store)[:10:-1],
        'office_sales': office_sales,
        'furniture_sales': furniture_sales,
        'tech_sales': tech_sales,
        'store': store,
    })


def inventory(request, item_filter):
    user = request.user
    store = Store.objects.filter(storeOwner=user.id)
    item_set = item_filter.lower()

    if item_set == 'all':
        items = Item.objects.filter(store__in=store).all()
    else:
        items = Item.objects.filter(store__in=store).order_by(f'{item_set}').all()

    return render(request, 'Main/Landing/inventory.html', {
        'user': user,
        'all_items': items,
        'items': items[:20]
    })


def create_item(request):
    user = request.user
    store = Store.objects.filter(storeOwner=user)

    if request.method == 'POST':
        item = Item(
            item_name=request.POST.get('item_name', ''),
            item_price=request.POST.get('item_price', ''),
            expense=request.POST.get('expense', ''),
            category=request.POST.get('category', ''),
            date_ordered=request.POST.get('date_ordered', ''),
            quantity=request.POST.get('quantity', ''),
            store=store[0]
        )
        item.save()

        return HttpResponseRedirect(reverse('inventory', args=['all']))


def update_item(request, item_id):
    if request.method == 'POST':
        item = Item.objects.get(id=item_id)
        item.item_name = request.POST.get('item_name', '')
        item.item_price = request.POST.get('item_price', 1)
        item.category = request.POST.get('category', '')
        item.date_ordered = request.POST.get('date_ordered', None)
        item.quantity = request.POST.get('quantity', '')
        item.save()

    return HttpResponseRedirect(reverse('inventory', args=['all']))


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()

    return HttpResponseRedirect(reverse('inventory', args=['all']))


def accounting(request, filter_data):
    user = request.user
    store = Store.objects.filter(storeOwner=user)
    items = Item.objects.filter(store__in=store).all()[:20]

    return render(request, 'Main/Landing/accounting.html', {
        'user': user,
        'panel': filter_data.capitalize(),
        'items': items,
        'item_tail': Item.objects.filter(store__in=store).all()[:5:-1]
    })


def profile(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_pass')

        if password == confirm_pass:
            user = User.objects.get(id=request.user.id)
            user.set_password(password)
            user.save()

            return HttpResponseRedirect(reverse('profile'))
    else:
        return render(request, 'Main/Landing/profile.html', {
            'user': request.user,
            'store': Store.objects.filter(storeOwner=request.user.id),
            'username': request.user.username
        })


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
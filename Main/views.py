import sys
import os
import pandas as pd
import csv
sys.path.append('..')

from django.db import IntegrityError
from django.template.defaultfilters import floatformat
from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Store, Address, Item, Sale, UserProfile
from datetime import datetime
from datetime import date
import random


# Create your views here.
def home(request):
    context = {}
    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        context['message'] = f"Hello, {first_name} {last_name}!"
    else:
        context['message'] = " "

    return render(request, 'Main/Login/home.html', context)

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
            try:
                user = User.objects.get(username=username)
                error_message = "Wrong Password. Please enter the correct password."

            except User.DoesNotExist:
                error_message = 'User does not exist. Please enter a valid username or register first.'

            return render(request, 'Main/Login/login.html', {'error': error_message})
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

            newUser.save()
            new_address.save()

            new_store = Store(storeName=store_name, storeAddress=store_address, storeOwner=newUser)
            new_store.save()

        except IntegrityError:
            return render(request, 'Main/Login/register.html', {
                'error_message': 'User already exists.'
            })

        # login(request, newUser)
        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'Main/Login/register.html')


# VIEWS FOR LOGGED IN USERS
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    store = Store.objects.get(storeOwner=user.id)
    items = Item.objects.filter(store=store).all()
    sales = Sale.objects.filter(store=store).all()
    
    monthly_sales = [
        get_sum_of_sales(Sale.objects.filter(date__month='01', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='02', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='03', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='04', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='05', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='06', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='07', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='08', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='09', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='10', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='11', store=store).all()),
        get_sum_of_sales(Sale.objects.filter(date__month='12', store=store).all())
    ]

    top_sales = check_top_sales(Sale.objects.filter(store=store).all())

    revenue = 0
    total_sales = 0
    total_expenses = 0
    net_income = 0

    # expenses
    for item in items:
        total_expenses += item.expense * item.quantity

    # revenue
    for sale in sales:
        total_sales += sale.item.item_price * sale.amount
        net_income += (sale.item.item_price - sale.item.expense) * sale.amount

    return render(request, 'Main/Landing/dashboard.html', {
        'user': user,
        'sales': intcomma(floatformat(total_sales, 2)),
        'revenue': intcomma(floatformat(revenue, 2)),
        'expense': intcomma(floatformat(total_expenses, 2)),
        'net_income': intcomma(floatformat(net_income, 2)),
        'all_items': items,
        'all_sales': sales,
        'monthly_sales': monthly_sales,
        'top_sales': top_sales,
        'store': store,
        'user_profile': user_profile,
        'recent_items' : Item.objects.filter(store=store),
        'recent_sales': Sale.objects.filter(store=store)
    })


def inventory(request, item_filter):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    store = Store.objects.filter(storeOwner=user.id)
    item_set = item_filter.lower()

    if request.method == 'POST':
        searched = Item.objects.filter(store__in=store, item_name__contains=request.POST.get('searched_items')).all()

        print(searched)

        return render(request, 'Main/Landing/inventory.html', {
            'user': user,
            'all_items': searched,
            'items': searched[:20]
        })

    if item_set == 'all':
        items = Item.objects.filter(store__in=store).all()
    else:
        items = Item.objects.filter(store__in=store).order_by(f'{item_set}').all()

    return render(request, 'Main/Landing/inventory.html', {
        'user': user,
        'all_items': items,
        'items': items[:20],
        'user_profile': user_profile
    })


def create_item(request):
    user_store = Store.objects.get(storeOwner=request.user.id)

    if request.method == 'POST':
        item = Item(
            item_name=request.POST.get('item_name', ''),
            item_price=request.POST.get('item_price', ''),
            expense=request.POST.get('expense', ''),
            category=request.POST.get('category', ''),
            date_ordered=request.POST.get('date_ordered', ''),
            quantity=request.POST.get('quantity', ''),
            store=user_store
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
    item.is_deleted = True
    item.save()

    return HttpResponseRedirect(reverse('inventory', args=['all']))


def reduce_item_quantity(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        item = Item.objects.get(id=item_id)
        item.quantity -= quantity
        item.save()

        new_sale = Sale(
            item=item,
            amount=quantity,
            store=Store.objects.get(storeOwner=request.user.id),
            profit=(item.item_price - item.expense) * quantity
        )
        new_sale.save()

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
    store = Store.objects.get(storeOwner=request.user.id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_pass = request.POST.get('confirm_pass')

        user = User.objects.get(id=request.user.id)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        store_name = request.POST.get('store_name')
        addr = request.POST.get('store_address')

        if password and confirm_pass and password == confirm_pass:
            user.set_password(password)
            user.save()
            return HttpResponseRedirect(reverse('login'))
        
        user.first_name = first_name
        user.last_name = last_name
        store.storeName = store_name
        store.storeAddress = addr

        user.save()
        store.save()

        return HttpResponseRedirect(reverse('profile'))
    
    else:
        return render(request, 'Main/Landing/profile.html', {
            'user': request.user,
            'store': store.storeName,
            'username': request.user.username,
            'address': store.storeAddress,
            'user_profile': user_profile
        })


def terms_and_conditions(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'Main/Landing/termsandconditions.html', {
        'user_profile': user_profile,
    })


def upload_store_data(request):
    if request.method == 'POST':
        store = Store.objects.get(storeOwner=request.user.id)
        store_data = request.FILES.get('store_data')

        if not store_data.name.endswith('.csv'):
            return render(request, 'Main/Landing/inventory.html', {'error': 'Only CSV files are allowed.'})

        if store_data is not None:
            df = pd.read_csv(store_data)
            try:
                for i in df.index:
                    new_item = Item(
                        item_name=df['item_name'][i],
                        item_price=df['item_price'][i],
                        expense=df['expense'][i],
                        quantity=df['quantity'][i],
                        category=df['category'][i],
                        date_ordered=df['date_ordered'][i],
                        store=store
                    )
                    new_item.save()
            except:
                return render(request, 'Main/Landing/inventory.html', {'error': 'Please check your CSV file and try again.'})

        return HttpResponseRedirect(reverse('inventory', args=['all']))
    

def upload_image(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        if 'profile_image' in request.FILES:
            profile_image = request.FILES['profile_image']

            if profile_image.size > 2 * 1024 * 1024:
                return render(request, 'Main/Landing/profile.html', {'error': 'File size should be up to 2MB.'})
            
            if not profile_image.content_type.startswith('image/'):
                return render(request, 'Main/Landing/profile.html', {'error': 'Only image files are allowed.'})
            
            if profile_image.name.endswith('.gif'):
                return render(request, 'Main/Landing/profile.html', {'error': 'Only JPG, JPEG, and PNG are allowed.'})

            if user_profile.profile_image:
                os.remove(user_profile.profile_image.path)
            
            user_profile.profile_image = profile_image
            username = request.user.username
            filename, file_extension = os.path.splitext(profile_image.name)
            new_filename = f"{username}{file_extension}"
            user_profile.profile_image.name = new_filename
            user_profile.save()

    return HttpResponseRedirect(reverse('profile'))


def delete_data(request):
    items = Item.objects.all()
    items.delete()

    return HttpResponse('Items Deleted')


def check_top_sales(items):
    categs = [0, 0, 0, 0, 0, 0]

    for item in items:
        if item.item.category == 'Drinks':
            categs[0] += (item.item.item_price - item.item.expense) * item.amount
        elif item.item.category == 'Condiments':
            categs[1] += (item.item.item_price - item.item.expense) * item.amount
        elif item.item.category == 'Snacks':
            categs[2] += (item.item.item_price - item.item.expense) * item.amount
        elif item.item.category == 'Canned Goods':
            categs[3] += (item.item.item_price - item.item.expense) * item.amount
        elif item.item.category == 'Detergents':
            categs[4] += (item.item.item_price - item.item.expense) * item.amount
        elif item.item.category == 'Others':
            categs[5] += (item.item.item_price - item.item.expense) * item.amount

    return categs


def get_sum_of_sales(monthly_sales):
    total_sale = 0

    for sale in monthly_sales:
        total_sale += (sale.item.item_price - sale.item.expense) * sale.amount

    return total_sale


def export_items_to_csv(request):
    today = date.today().strftime('%Y-%m-%d')
    filename = f"{today}_ITEMS_REPORT.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Item Price', 'Expense', 'Quantity', 'Category', 'Date Ordered'])

    items = Item.objects.filter(store__storeOwner=request.user)

    for item in items:
        writer.writerow([item.item_name, item.item_price, item.expense, item.quantity, item.category, item.date_ordered])

    return response


def export_sales_to_csv(request):
    today = date.today().strftime('%Y-%m-%d')
    filename = f"{today}_SALES_REPORT.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Item Price', 'Category', 'Amount', 'Profit', 'Date'])

    sales = Sale.objects.filter(store__storeOwner=request.user)

    for sale in sales:
        item = sale.item
        writer.writerow([item.item_name, item.item_price, item.category, sale.amount, sale.profit, sale.date])

    return response
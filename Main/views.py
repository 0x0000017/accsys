from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    else:
        return render(request, 'Main/login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']
        email = request.POST['email']

        if password != confirm:
            return render(request, 'Main/register.html', {
                'error_message': 'Passwords do not match.'
            })

        try:
            newUser = User(username=username, password=password, email=email)
            newUser.save()
        except IntegrityError:
            return render(request, 'Main/register.html', {
                'error_message': 'User already exists.'
            })

        login(request, newUser)
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'Main/register.html')


def dashboard(request):
    user = request.user
    return HttpResponse(f'Hello, {user.username}!')
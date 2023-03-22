from django.urls import path
from django.contrib.auth.views import LogoutView

from AccSys import settings
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory', views.inventory, name='inventory'),
    path('accounting', views.accounting, name='accounting'),
    path('profile', views.profile, name='profile'),
    path('help', views.help, name='help'),
]
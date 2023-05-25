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
    path('inventory/<str:item_filter>', views.inventory, name='inventory'),
    path('create_item', views.create_item, name='create_item'),
    path('update_item/<int:item_id>', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('accounting/<str:filter_data>', views.accounting, name='accounting'),
    path('profile', views.profile, name='profile'),
    path('help', views.help, name='help'),
    path('generate_data', views.generate_data, name='generate'),
    path('delete', views.delete_data, name='delete')
]
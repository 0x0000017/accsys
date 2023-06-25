from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from AccSys import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('inventory/<str:item_filter>', views.inventory, name='inventory'),
    path('upload_csv', views.upload_store_data, name='upload_store_data'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('create_item', views.create_item, name='create_item'),
    path('update_item/<int:item_id>', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('reduce_item_quantity/<int:item_id>', views.reduce_item_quantity, name='reduce_items'),
    path('accounting/<str:filter_data>', views.accounting, name='accounting'),
    path('profile', views.profile, name='profile'),
    path('terms_and_conditions', views.terms_and_conditions, name='terms'),
    path('delete', views.delete_data, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



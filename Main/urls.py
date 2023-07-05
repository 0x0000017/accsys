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
    path('upload_db', views.upload_store_data, name='upload_store_data'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('create_item', views.create_item, name='create_item'),
    path('update_item/<int:item_id>', views.update_item, name='update_item'),
    path('delete_item/<int:item_id>', views.delete_item, name='delete_item'),
    path('reduce_item_quantity/<int:item_id>', views.reduce_item_quantity, name='reduce_items'),
    path('profile', views.profile, name='profile'),
    path('terms_and_conditions', views.terms_and_conditions, name='terms'),
    path('data_privacy_policy', views.data_privacy_policy, name='dpp'),
    path('delete', views.delete_data, name='delete'),
    path('export-items', views.export_items_to_csv, name='export-items'),
    path('export-items-xls/', views.export_items_to_excel, name='export-items-xls'),
    path('export-sales', views.export_sales_to_csv, name='export-sales'),
    path('export-sales-xls/', views.export_sales_to_excel, name='export-sales-xls'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('generate-item/', views.generate_item_report, name='generate_item_report'),
    path('generate-sales/', views.generate_sales_report, name='generate_sales_report'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



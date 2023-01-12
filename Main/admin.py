from django.contrib import admin
from .models import Category, Item, Sale, Store

# Register your models here.
admin.site.register(Category),
admin.site.register(Item),
admin.site.register(Sale),
admin.site.register(Store),

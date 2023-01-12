from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)


class Store(models.Model):
    storeName = models.CharField(max_length=200)
    storeOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_owner')
    storeAddress = models.CharField(max_length=200)
    date_registered = models.DateTimeField(auto_now=True)


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_price = models.IntegerField()
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat')
    date_ordered = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='location')


class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='product')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)




from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Store(models.Model):
    storeName = models.CharField(max_length=200)
    storeOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_owner')
    storeAddress = models.CharField(max_length=200)
    date_registered = models.DateTimeField(auto_now=True)


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_price = models.IntegerField()
    expense = models.IntegerField()
    quantity = models.IntegerField()
    category = models.CharField(max_length=64)
    date_ordered = models.DateTimeField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='location')


class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='product')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sale_location')


class Address(models.Model):
    address_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')
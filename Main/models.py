from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Store(models.Model):
    storeName = models.CharField(max_length=200)
    storeOwner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_owner')
    storeAddress = models.CharField(max_length=200)
    date_registered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.storeName


class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=64)
    date_ordered = models.DateField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='location')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name


class Sale(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='product')
    amount = models.IntegerField()
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='sale_location')

    def __str__(self):
        return f"Sale of {self.item} ({self.date})"


class Address(models.Model):
    address_name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_address')



# TESTING
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
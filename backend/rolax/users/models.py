from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    manager = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='managed_users')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Items(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='owned_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class sellReciept(models.Model):
    recieptNumber = models.IntegerField()
    item = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True, related_name='sell_receipts')
    quantity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sell_receipts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class purchaseReciept(models.Model):
    recieptNumber = models.IntegerField()
    item = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_receipts')
    quantity = models.IntegerField( default=0 , null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='purchase_receipts')
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

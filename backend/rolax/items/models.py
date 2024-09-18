"""
module to store items model
"""

from django.db import models
from users.models import User


class Items(models.Model):
    """
    model to store items
    """

    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, unique=True)
    price = models.FloatField()
    quantity = models.IntegerField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="owned_items",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [("manage_items", "Can manage items")]

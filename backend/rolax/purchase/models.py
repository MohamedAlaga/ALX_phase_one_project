"""
moudle to store purchase receipt
"""

from django.db import models
from users.models import User
from items.models import Items


class purchaseReciept(models.Model):
    """
    model to store purchase receipt
    """

    recieptNumber = models.IntegerField()
    item = models.ForeignKey(
        Items,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="purchase_receipts",
    )
    quantity = models.IntegerField(default=0, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="purchase_receipts",
    )
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [("manage_purchase_receipts", "Can manage purchase receipts")]

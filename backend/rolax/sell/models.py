"""
module for sell receipt model
"""

from django.db import models
from users.models import User
from items.models import Items


class sellReciept(models.Model):
    """
    model to store sell receipt
    """

    recieptNumber = models.IntegerField()
    item = models.ForeignKey(
        Items,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sell_receipts",
    )
    quantity = models.IntegerField()
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sell_receipts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [("manage_sell_receipts", "Can manage sell receipts")]

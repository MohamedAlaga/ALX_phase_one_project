"""
module to serialize purchase receipt
"""

from rest_framework import serializers
from items.models import Items
from .models import purchaseReciept


class PurchaseReceiptSerializer(serializers.ModelSerializer):
    """
    serializer for purchase receipt
    """

    class Meta:
        """
        class to define the model and fields to be serialized
        """

        model = purchaseReciept
        fields = ["item", "quantity", "price", "owner", "recieptNumber"]

    def create(self, validated_data):
        """
        method to create a purchase receipt

        Returns:
            on success : purchase receipt
        """
        purchase_receipt = purchaseReciept.objects.create(
            recieptNumber=validated_data["recieptNumber"],
            item=validated_data["item"],
            quantity=validated_data["quantity"],
            owner=validated_data["owner"],
            price=validated_data["price"],
        )
        Items.objects.filter(id=validated_data["item"].id).update(
            quantity=validated_data["item"].quantity + validated_data["quantity"]
        )
        return purchase_receipt

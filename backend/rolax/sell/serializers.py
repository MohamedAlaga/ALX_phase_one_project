"""
moduel to serialize sell receipt
"""

from rest_framework import serializers
from items.models import Items
from .models import sellReciept


class SellReceiptSerializer(serializers.ModelSerializer):
    """
    serializer for sell receipt
    """

    class Meta:
        """
        class to define the model and fields to be serialized
        """

        model = sellReciept
        fields = ["item", "quantity", "owner", "recieptNumber"]

    def create(self, validated_data):
        """
        method to create a sell receipt

        Returns:
            on success : sell receipt
        """
        sell_receipt = sellReciept.objects.create(
            recieptNumber=validated_data["recieptNumber"],
            item=validated_data["item"],
            quantity=validated_data["quantity"],
            owner=validated_data["owner"],
        )
        Items.objects.filter(id=validated_data["item"].id).update(
            quantity=validated_data["item"].quantity - validated_data["quantity"]
        )
        return sell_receipt

"""
module to serialize item
"""

from rest_framework import serializers
from .models import Items


class ItemsSerializer(serializers.ModelSerializer):
    """
    serializer for item
    """

    class Meta:
        """
        class to define the model and fields to be serialized
        """

        model = Items
        fields = ["id", "name", "barcode", "price", "owner"]

    def create(self, validated_data):
        """
        method to create an item

        Returns:
            on success : instance of the new item
        """
        instance = self.Meta.model(**validated_data)
        instance.quantity = 0
        instance.save()
        return instance

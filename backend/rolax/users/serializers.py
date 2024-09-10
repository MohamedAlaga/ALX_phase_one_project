from rest_framework import serializers
from .models import User, Items


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        instance.manager = instance
        instance.save()
        return instance


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["id", "name", "barcode", "price", "owner"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.quantity = 0
        instance.save()
        return instance

class BuyReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["id", "name", "barcode", "price", "quantity", "owner"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

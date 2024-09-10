from rest_framework import serializers
from .models import User, Items , purchaseReciept


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

class PurchaseReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = purchaseReciept
        fields = ['item', 'quantity', 'price' , 'owner', 'recieptNumber']

    def create(self, validated_data):
        purchase_receipt = purchaseReciept.objects.create(
            recieptNumber=validated_data['recieptNumber'],
            item=validated_data['item'],
            quantity=validated_data['quantity'],
            owner = validated_data['owner'],
            price=validated_data['price']
        )
        Items.objects.filter(id=validated_data['item'].id).update(quantity=validated_data['item'].quantity + validated_data['quantity'])
        return purchase_receipt

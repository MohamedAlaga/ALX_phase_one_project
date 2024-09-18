"""
module to serialize the user model
"""

from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for new users (new pharmacy managers)
    """

    class Meta:
        """
        class to define the model and fields to be serialized
        """

        model = User
        fields = ["id", "name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        method to create a new user

        Args:
            validated_data (dict): user data to be validated

        returns:
            instance : the new user instance
        """
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        instance.manager = instance
        permissions = [
            "manage_users",
            "manage_items",
            "manage_sell_receipts",
            "manage_purchase_receipts",
        ]
        instance.save()
        for perm in permissions:
            instance.user_permissions.add(Permission.objects.get(codename=perm))
        return instance

    def update(self, instance, validated_data):
        """
        method to update a user instance

        Args:
            instance (user): user instance to be updated

        Returns:
            instance : the updated user instance
        """
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class SubUserSerializer(serializers.ModelSerializer):
    """
    serializer for sub users (pharmacy employees)
    """

    class Meta:
        """
        class to define the model and fields to be serialized
        """

        model = User
        fields = ["id", "name", "email", "password", "manager"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        method to create a new sub user

        Args:
            validated_data (dict): user data to be validated

        returns:
            instance : the new subuser instance
        """
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

"""
module to handle items views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.views import checkUser
from .serializers import ItemsSerializer
from .models import Items


class addItemsView(APIView):
    """
    end node to add items
    """

    def post(self, request):
        """
        method to add items

        Args:
            request (dict): dictionary containing item name, quantity and price
                example: {"name": "item1", "barcode": "6549987123", "price": 20}

        Returns:
            on success: message: "Item added successfully"
            on failure: error message and status code 400 or 403
        """
        try:
            user = checkUser(request.COOKIES.get("token"))
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.has_perm("users.manage_items"):
            return Response(
                {"message": "You do not have permission to add items"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.manager.id
        data = request.data.copy()
        data["owner"] = owner
        serizlizer = ItemsSerializer(data=data)
        serizlizer.is_valid(raise_exception=True)
        serizlizer.save()

        return Response(serizlizer.data)


class getCurrentUserItems(APIView):
    """
    end point to get all items of the current pharmacy
    """

    def get(self, request):
        """
        method to get all items of the current pharmacy

        Returns:
            on success: list of items
            on failure: error message and status code 400 or 403
        """
        try:
            user = checkUser(request.COOKIES.get("token"))
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.has_perm("users.manage_items"):
            return Response(
                {"message": "You do not have permission to  items"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.id
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        items = Items.objects.filter(owner=owner)
        data = []
        if items:
            for item in items:
                data.append(
                    {
                        "item_id": item.id,
                        "item_name": item.name,
                        "quantity": item.quantity,
                        "price": item.price,
                        "owner": item.owner.id,
                    }
                )
            return Response(data)
        return Response({"message": "No items found"}, status=status.HTTP_404_NOT_FOUND)


class getCurrentUserItemsById(APIView):
    """
    end point to get items by id
    """

    def get(self, request, id):
        """
        method to get items by id

        Args:
            id (int): item id

        Returns:
            on success: list of items
            on failure: error message and status code 404 or 403
        """
        try:
            owner = checkUser(request.COOKIES.get("token")).id
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        item = Items.objects.filter(owner=owner, id=id).first()
        if item:
            return Response(
                {
                    "item_id": item.id,
                    "item_name": item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "owner": item.owner.id,
                }
            )
        return Response({"message": "No items found"}, status=status.HTTP_404_NOT_FOUND)


class getCurrentUserItemsBybarcode(APIView):
    """
    end point to get items by barcode
    """

    def get(self, request, barcode):
        """
        method to get items by barcode

        Args:
            barcode (string): barcode of the item
        Returns:
            on success: item details
            on failure: error message and status code 404 or 403
        """
        try:
            owner = checkUser(request.COOKIES.get("token")).id
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        item = Items.objects.filter(owner=owner, barcode=barcode).first()
        if item:
            return Response(
                {
                    "item_id": item.id,
                    "item_name": item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "owner": item.owner.id,
                }
            )
        return Response({"message": "No items found"}, status=status.HTTP_404_NOT_FOUND)


class getSearchItems(APIView):
    """
    end point to search items by name
    """

    def get(self, request, name):
        """
        method to search items by name

        Args:
            name (string): name of the item

        Returns:
            on success: list of items
            on failure: error message and status code 404 or 403
        """
        try:
            owner = checkUser(request.COOKIES.get("token")).id
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        items = Items.objects.filter(owner=owner, name__icontains=name)
        data = []
        if items:
            for item in items:
                data.append(
                    {
                        "item_id": item.id,
                        "barcode": item.barcode,
                        "item_name": item.name,
                        "quantity": item.quantity,
                        "price": item.price,
                        "owner": item.owner.id,
                    }
                )
            return Response(data)
        return Response({"message": "No items found"}, status=status.HTTP_404_NOT_FOUND)

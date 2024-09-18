"""
module to handle purchase receipt views
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from items.models import Items
from .models import purchaseReciept
from users.views import checkUser
from .serializers import PurchaseReceiptSerializer


class purchaseReceiptBulkCreateView(APIView):
    """
    end point to create receipt purchase mutilple items at once
    """

    def post(self, request):
        """
        method to create purchase receipt for multiple items at once

        Args:
            request (list): list of dictionaries containing item id, quantity and price
                example: [{"id": "1", "quantity": 2, "price": 2000}, {"id": "2", "quantity": 3, "price": 3000}]
        Returns:
            on success: message: "Purchase receipts created successfully"
            on failure: error message and status code 400 or 403
        """
        user = checkUser(request.COOKIES.get("token"))
        if not user.has_perm("users.manage_purchase_receipts"):
            return Response(
                {"message": "You do not have permission to purchase receipt"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.manager.id
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        data = request.data.copy()
        last_receipt = purchaseReciept.objects.filter(owner=owner).last()
        recieptNumber = last_receipt.recieptNumber + 1 if last_receipt else 1
        for item_data in data:
            try:
                item = Items.objects.get(id=item_data["id"])
                if item.owner.id != owner:
                    return Response(
                        {
                            "error": f"Item with id {item_data['id']} does not belong to you"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Items.DoesNotExist:
                return Response(
                    {"error": f"Item with id {item_data['id']} does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer_data = {
                "item": item.id,
                "quantity": item_data["quantitiy"],
                "price": item_data["price"],
                "owner": owner,
                "recieptNumber": recieptNumber,
            }
            serializer = PurchaseReceiptSerializer(
                data=serializer_data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Purchase receipts created successfully"},
            status=status.HTTP_201_CREATED,
        )


class getCurentUserlastPurchaseReciept(APIView):
    """
    end point to get the last purchase receipt for the current user
    """

    def get(self, request):
        """
        get the last purchase receipt for the current user

        Returns:
            on success: list of items in the last purchase receipt
            on failure: error message and status code 404 or 403
        """
        user = checkUser(request.COOKIES.get("token"))
        if not user.has_perm("users.manage_purchase_receipts"):
            return Response(
                {"message": "You do not have permission to purchase receipts"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.manager.id
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        last_receipt = purchaseReciept.objects.filter(owner=owner).last()
        if last_receipt:
            reciepts = purchaseReciept.objects.filter(
                recieptNumber=last_receipt.recieptNumber, owner=owner
            )
            data = []
            for reciept in reciepts:
                data.append(
                    {
                        "item_id": reciept.item.id,
                        "item_name": reciept.item.name,
                        "quantity": reciept.quantity,
                        "price": reciept.price,
                        "owner": reciept.owner.id,
                        "recieptNumber": reciept.recieptNumber,
                        "date": reciept.created_at,
                    }
                )
            return Response(data)
        return Response(
            {"message": "No purchase receipt found"}, status=status.HTTP_404_NOT_FOUND
        )


class getUserPurchaserecieptsByNumber(APIView):
    """
    end point to get purchase receipt by reciept number
    """

    def get(self, request, id):
        """
        get purchase receipt by reciept number

        Args:
            id (int): reciept number

        Returns:
            on success: list of items in the purchase receipt
            on failure: error message and status code 404 or 403
        """
        user = checkUser(request.COOKIES.get("token"))
        if not user.has_perm("users.manage_purchase_receipts"):
            return Response(
                {"message": "You do not have permission to purchase receipt"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.id
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        reciepts = purchaseReciept.objects.filter(recieptNumber=id, owner=owner)
        data = []
        if reciepts:
            for reciept in reciepts:
                data.append(
                    {
                        "item_id": reciept.item.id,
                        "item_name": reciept.item.name,
                        "quantity": reciept.quantity,
                        "price": reciept.price,
                        "owner": reciept.owner.id,
                        "recieptNumber": reciept.recieptNumber,
                        "date": reciept.created_at,
                    }
                )
            return Response(data)
        return Response(
            {"message": "No purchase receipt found"}, status=status.HTTP_404_NOT_FOUND
        )

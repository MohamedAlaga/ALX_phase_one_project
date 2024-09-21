"""
module to handle sell receipt views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from items.models import Items
from .models import sellReciept
from users.views import checkUser
from .serializers import SellReceiptSerializer


class sellReceiptBulkCreateView(APIView):
    """
    end point to create receipt sell mutilple items at once
    """

    def post(self, request):
        """
        method to create sell receipt for multiple items at once

        Args:
            request (list): list of dictionaries containing item id and quantity
                example: [{"id": "1", "quantity": 2}, {"id": "2", "quantity": 3}]

        Returns:
            on success: message: "Sell receipts created successfully"
            on failure: error message and status code 400 or 403
        """
        try:
            user = checkUser(request.COOKIES.get("token"))
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.has_perm("users.manage_sell_receipts"):
            return Response(
                {"message": "You do not have permission to sell receipt"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.id
        data = request.data.copy()
        last_receipt = sellReciept.objects.filter(owner=owner).last()
        recieptNumber = last_receipt.recieptNumber + 1 if last_receipt else 1
        for item_data in data:
            try:
                item = Items.objects.get(id=item_data["id"])
                if item.owner.id != int(owner):
                    return Response(
                        {
                            "error": f"Item with id {item_data['id']} does not belong to you your id is {owner} and it blongs to {item.owner.id}"
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
                "owner": owner,
                "recieptNumber": recieptNumber,
            }
            serializer = SellReceiptSerializer(
                data=serializer_data, context={"request": request}
            )
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Sell receipts created successfully"},
            status=status.HTTP_201_CREATED,
        )


class getCurrentUserLastsellReceipt(APIView):
    """
    end point to get the last sell receipt for the current user
    """

    def get(self, request):
        """
        method to get the last sell receipt for the current user

        Returns:
            on success: list of items in the last sell receipt
            on failure: error message and status code 404 or 403
        """
        try:
            user = checkUser(request.COOKIES.get("token"))
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.has_perm("users.manage_sell_receipts"):
            return Response(
                {"message": "You do not have permission to sell receipt"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.id
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        last_receipt = sellReciept.objects.filter(owner=owner).last()
        if last_receipt:
            reciepts = sellReciept.objects.filter(
                recieptNumber=last_receipt.recieptNumber, owner=owner
            )
            data = []
            for reciept in reciepts:
                data.append(
                    {
                        "item_id": reciept.item.id,
                        "item_name": reciept.item.name,
                        "quantity": reciept.quantity,
                        "price": reciept.item.price * reciept.quantity,
                        "owner": reciept.owner.id,
                        "recieptNumber": reciept.recieptNumber,
                        "date": reciept.created_at,
                    }
                )
            return Response(data)
        return Response(
            {"message": "No purchase receipt found"}, status=status.HTTP_404_NOT_FOUND
        )


class getCurrentUserSellRecieptsByNumber(APIView):
    """
    end point to get the sell receipt for the current user by receipt number
    """

    def get(self, request, id):
        """
        method to get the sell receipt for the current user by receipt number

        Args:
            id (int): receipt number

        Returns:
            on success: list of items in the sell receipt
            on failure: error message and status code 404 or 403
        """
        try:
            user = checkUser(request.COOKIES.get("token"))
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.has_perm("users.manage_sell_receipts"):
            return Response(
                {"message": "You do not have permission to sell receipt"},
                status=status.HTTP_403_FORBIDDEN,
            )
        owner = user.id
        if owner is None:
            return Response(
                {"message": "No user found"}, status=status.HTTP_403_FORBIDDEN
            )
        reciepts = sellReciept.objects.filter(recieptNumber=id, owner=owner)
        data = []
        if reciepts:
            for reciept in reciepts:
                data.append(
                    {
                        "item_id": reciept.item.id,
                        "item_name": reciept.item.name,
                        "quantity": reciept.quantity,
                        "price": reciept.item.price * reciept.quantity,
                        "owner": reciept.owner.id,
                        "recieptNumber": reciept.recieptNumber,
                        "date": reciept.created_at,
                    }
                )
            return Response(data)
        return Response(
            {"message": "No purchase receipt found"}, status=status.HTTP_404_NOT_FOUND
        )

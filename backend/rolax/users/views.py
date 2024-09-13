from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import (
    UserSerializer,
    ItemsSerializer,
    PurchaseReceiptSerializer,
    SellReceiptSerializer,
    SubUserSerializer,
)
from .models import User, Items, purchaseReciept, sellReciept
from rest_framework import status
import jwt, datetime
from django.contrib.auth.models import Permission


def checkUser(token):
    if not token:
        raise AuthenticationFailed("Unauthenticated!")

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")

    user = User.objects.filter(id=payload["id"]).first()
    return user


class Register(APIView):
    def post(self, request):
        serizlizer = UserSerializer(data=request.data)
        serizlizer.is_valid(raise_exception=True)
        serizlizer.save()
        return Response(serizlizer.data)


class RegisterSubUser(APIView):
    def post(self, request):
        manager = request.COOKIES.get("pharma_id")
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to create sub users"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not manager:
            return Response(
                {"message": "No manager found"}, status=status.HTTP_403_FORBIDDEN
            )
        if currentUser:
            data = request.data.copy()
            data["manager"] = manager
            serizlizer = SubUserSerializer(data=data)
            serizlizer.is_valid(raise_exception=True)
            serizlizer.save()
            return Response(serizlizer.data)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class GrantPermission(APIView):
    def post(self, request):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to grant permissions"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user_id = request.data["user_id"]
        if not user_id:
            return Response(
                {"message": "No user id found"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.filter(id=user_id).first()
        if user:
            permission = request.data["permission"]
            if not permission:
                return Response(
                    {"message": "No permission found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.user_permissions.add(Permission.objects.get(codename=permission))
            return Response({"message": "Permission granted successfully"})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class RevokePermission(APIView):
    def post(self, request):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to revoke permissions"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user_id = request.data["user_id"]
        user = User.objects.filter(id=user_id).first()
        if user:
            permission = request.data["permission"]
            if not permission:
                return Response(
                    {"message": "No permission found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.user_permissions.remove(Permission.objects.get(codename=permission))
            return Response({"message": "Permission revoked successfully"})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class manageUser(APIView):
    def get(self, request, id):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to manage users"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = User.objects.filter(id=id, manager=currentUser.manager).first()
        if user:
            serizlizer = UserSerializer(user)
            return Response(serizlizer.data)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to delete users"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return Response({"message": "User deleted successfully"})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to update users"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = User.objects.filter(id=id).first()
        if user:
            serizlizer = UserSerializer(user, data=request.data, partial=True)
            serizlizer.is_valid(raise_exception=True)
            serizlizer.save()
            return Response(serizlizer.data)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class getCurrentUserPerms(APIView):
    def get(self, request):
        currentUser = checkUser(request.COOKIES.get("token"))
        if currentUser:
            perms = currentUser.get_all_permissions()
            return Response({"permissions": perms})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class getuserPerms(APIView):
    def get(self, request, id):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to view user permissions"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user = User.objects.filter(id=id, manager=currentUser.manager).first()
        if user:
            perms = user.get_all_permissions()
            return Response({"permissions": perms})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class getAllUsers(APIView):
    def get(self, request):
        currentUser = checkUser(request.COOKIES.get("token"))
        if not currentUser.has_perm("users.manage_users"):
            return Response(
                {"message": "You do not have permission to view users"},
                status=status.HTTP_403_FORBIDDEN,
            )
        users = User.objects.filter(manager=currentUser.manager)
        data = []
        for user in users:
            data.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "manager": user.manager.id,
                }
            )
        return Response(data)


class Login(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="token", value=token, httponly=True)
        response.data = {"token": token, "pharma_id": user.manager.id}

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("token")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.filter(id=payload["id"]).first()
        serizlizer = UserSerializer(user)
        return Response(serizlizer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("token")
        response.data = {"message": "success"}
        return response


class addItemsView(APIView):
    def post(self, request):
        user = checkUser(request.COOKIES.get("token"))
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


class purchaseReceiptBulkCreateView(APIView):
    def post(self, request):
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
    def get(self, request):
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
    def get(self, request, id):
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


class sellReceiptBulkCreateView(APIView):
    def post(self, request):
        user = checkUser(request.COOKIES.get("token"))
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
    def get(self, request):
        user = checkUser(request.COOKIES.get("token"))
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
    def get(self, request, id):
        user = checkUser(request.COOKIES.get("token"))
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


class getCurrentUserItems(APIView):
    def get(self, request):
        user = checkUser(request.COOKIES.get("token"))
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
    def get(self, request, id):
        owner = checkUser(request.COOKIES.get("token")).id
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
    def get(self, request, barcode):
        owner = checkUser(request.COOKIES.get("token")).id
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
    def get(self, request, name):
        owner = checkUser(request.COOKIES.get("token")).id
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

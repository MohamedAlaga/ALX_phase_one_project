"""
view Module to authenticate users.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import (
    UserSerializer,
    SubUserSerializer,
)
from .models import User
from rest_framework import status
import jwt, datetime
from django.contrib.auth.models import Permission


def checkUser(token):
    """
    return user object from token

    Args:
        token (string): user authentication token

    Raises:
        AuthenticationFailed: if the token expired or empty

    Returns:
        user: current user object
    """
    if not token:
        raise AuthenticationFailed("Unauthenticated!")

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")

    user = User.objects.filter(id=payload["id"]).first()
    return user


class Register(APIView):
    """
    end node to register new user
    """

    def post(self, request):
        """post method to register new user

        Args:
            request (dict): dictionary of users data
                example:{name: "name", email: "email", password: "password"}

        Returns:
            on success: user object
            on failure: error message & status code 400
        """
        try:
            serizlizer = UserSerializer(data=request.data)
            serizlizer.is_valid(raise_exception=True)
            serizlizer.save()
            return Response(serizlizer.data)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterSubUser(APIView):
    """
    end node to register new sub user
    """

    def post(self, request):
        """
        post method to register new sub user to current user

        Args:
            request (dict): dictionary of users data
                example:{name: "name", email: "email", password: "password"}
        Returns:
            onsucces: user object
            onfailure: error message & status code 403 or 404
        """
        currentUser = checkUser(request.COOKIES.get("token"))
        manager = currentUser.manager.id
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
    """
    end node to grant permission to user
    """

    def post(self, request):
        """post method to grant permission to user

        Args:
            request (dict): permission data
                example:{permission: "manage_sell_receipts", user_id: 26}

        Returns:
            on success: permission granted successfully
            on failure: error message & status code 400 or 404
        """
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
    """
    end node to revoke permission from user
    """

    def post(self, request):
        """
        end node to revoke permission from user

        Args:
            request (dict): permission data
                example:{permission: "manage_sell_receipts", user_id: 26}

        Returns:
            on success: permission revoked successfully
            on failure: error message & status code 400 or 404
        """
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
    """
    end node to manage operarions user
    """

    def get(self, request, id):
        """
        get method to get user by id

        Args:
            id (int): user id

        Returns:
            on success: user object
            on failure: error message & status code 404 or 403
        """
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
        """
        delete method to delete user by id

        Args:
            id (int): user id

        Returns:
            on success: user deleted successfully
            on failure: error message & status code 404 or 403
        """
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
    """
    end node to get current user permissions
    """

    def get(self, request):
        """get method to get current user permissions

        Returns:
            on success: dictonary contains user permissions
            on failure: error message & status code 404
        """
        currentUser = checkUser(request.COOKIES.get("token"))
        if currentUser:
            perms = currentUser.get_all_permissions()
            return Response({"permissions": perms})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class getuserPerms(APIView):
    """
    end node to get user permissions by id
    """

    def get(self, request, id):
        """
        get method to get user permissions by id

        Args:
            id (int): user id

        Returns:
            on success: dictonary contains user permissions
            on failure: error message & status code 404
        """
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
    """
    end node to get all Pharmacy users

    """

    def get(self, request):
        """
        get method to get all Pharmacy users

        Returns:
            on success: list of all users
            on failure: error message & status code 403
        """
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
    """
    end node to login user
    """

    def post(self, request):
        """post method to login user

        Args:
            request (dict): dictionary of users data
                example:{email: "email", password: "password"}

        Raises:
            AuthenticationFailed: if the user not found or password incorrect

        Returns:
            on success: user token
            on failure: error message & status code 400
        """
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
    """
    end node to get user by token
    """

    def get(self, request):
        """get method to get user by token

        Raises:
            AuthenticationFailed: if the token expired or empty

        Returns:
            on success: user object
            on failure: error message & status code 400
        """
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
    """
    end node to logout user
    """

    def post(self, request):
        """
        post method to logout user

        Returns:
            on success: success message
        """
        response = Response()
        response.delete_cookie("token")
        response.data = {"message": "success"}
        return response

from django.urls import path
from .views import *

urlpatterns = [
    path("", getAllUsers.as_view()),
    path("current", UserView.as_view()),
    path("add", RegisterSubUser.as_view()),
    path("<int:id>", manageUser.as_view()),
    path("perms/grant", GrantPermission.as_view()),
    path("perms/revoke", RevokePermission.as_view()),
    path("perms/current", getCurrentUserPerms.as_view()),
    path("perms/<int:id>", getuserPerms.as_view()),
    path("signup", Register.as_view()),
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
]

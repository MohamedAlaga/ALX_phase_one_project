from django.urls import path
from .views import *

urlpatterns = [
    # items
    path("items/add", addItemsView.as_view()),
    path("items", getCurrentUserItems.as_view()),
    path("items/<int:id>", getCurrentUserItemsById.as_view()),
    path("items/barcode/<str:barcode>", getCurrentUserItemsBybarcode.as_view()),
    path("items/search/<str:name>", getSearchItems.as_view()),
    # purchase
    path("purchase/add", purchaseReceiptBulkCreateView.as_view()),
    path("purchase/last", getCurentUserlastPurchaseReciept.as_view()),
    path("purchase/<int:id>", getUserPurchaserecieptsByNumber.as_view()),
    # sell
    path("sell/add", sellReceiptBulkCreateView.as_view()),
    path("sell/last", getCurrentUserLastsellReceipt.as_view()),
    path("sell/<int:id>", getCurrentUserSellRecieptsByNumber.as_view()),
    # users
    path("users", getAllUsers.as_view()),
    path("users/current", UserView.as_view()),
    path("users/add", RegisterSubUser.as_view()),
    path("users/<int:id>", manageUser.as_view()),
    path("users/perms/grant", GrantPermission.as_view()),
    path("users/perms/revoke", RevokePermission.as_view()),
    path("users/perms/current", getCurrentUserPerms.as_view()),
    path("users/perms/<int:id>", getuserPerms.as_view()),
    path("register", Register.as_view()),
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
]

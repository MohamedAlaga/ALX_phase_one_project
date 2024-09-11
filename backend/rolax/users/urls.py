from django.urls import path
from .views import *
urlpatterns = [
  path('register', Register.as_view()),
  path('login', Login.as_view()),
  path('user', UserView.as_view()),
  path('logout', Logout.as_view()),
  path('items/add', addItemsView.as_view()),
  path('purchase/add',purchaseReceiptBulkCreateView.as_view()),
  path('purchase/last', getCurentUserlastPurchaseReciept.as_view()),
  path('purchase/<int:id>', getUserPurchaserecieptsByNumber.as_view()),
  path('sell/add',sellReceiptBulkCreateView.as_view()),
  path('sell/last', getCurrentUserLastsellReceipt.as_view()),
  path('sell/<int:id>', getCurrentUserSellRecieptsByNumber.as_view()),
  path('items', getCurrentUserItems.as_view()),
  path('items/<int:id>', getCurrentUserItemsById.as_view()),
  path('items/barcode/<str:barcode>', getCurrentUserItemsBybarcode.as_view()),
  path('items/search/<str:name>', getSearchItems.as_view()),
]

from django.urls import path
from .views import Register , Login , UserView , Logout , addItemsView, purchaseReceiptBulkCreateView , getCurentUserlastPurchaseReciept , getUserPurchaserecieptsByNumber
urlpatterns = [
  path('register', Register.as_view()),
  path('login', Login.as_view()),
  path('user', UserView.as_view()),
  path('logout', Logout.as_view()),
  path('items/add', addItemsView.as_view()),
  path('purchase/add',purchaseReceiptBulkCreateView.as_view()),
  path('purchase/last', getCurentUserlastPurchaseReciept.as_view()),
  path('purchase/<int:id>', getUserPurchaserecieptsByNumber.as_view()),
]

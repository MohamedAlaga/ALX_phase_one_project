from django.urls import path
from .views import *

urlpatterns = [
    path("add", purchaseReceiptBulkCreateView.as_view()),
    path("last", getCurentUserlastPurchaseReciept.as_view()),
    path("<int:id>", getUserPurchaserecieptsByNumber.as_view()),
]

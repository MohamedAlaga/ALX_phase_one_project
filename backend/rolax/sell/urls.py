from django.urls import path
from .views import *

urlpatterns = [
    path("add", sellReceiptBulkCreateView.as_view()),
    path("last", getCurrentUserLastsellReceipt.as_view()),
    path("<int:id>", getCurrentUserSellRecieptsByNumber.as_view()),
]

from django.urls import path
from .views import *

urlpatterns = [
    path("add", addItemsView.as_view()),
    path("", getCurrentUserItems.as_view()),
    path("<int:id>", getCurrentUserItemsById.as_view()),
    path("barcode/<str:barcode>", getCurrentUserItemsBybarcode.as_view()),
    path("search/<str:name>", getSearchItems.as_view()),
]

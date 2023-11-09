from django.urls import path

from . import views

app_name = "adabank"

urlpatterns = [
    path("payment/", views.payment, name="payment"),
    path("transfer/", views.transfer_incoming, name="transfer_incoming"),
]

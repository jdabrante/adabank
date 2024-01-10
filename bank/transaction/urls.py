from django.urls import path

from . import views

app_name = "adabank"

urlpatterns = [
    path("incoming/", views.transfer_incoming, name="transfer_incoming"),
    path(
        "outcoming/<int:account_id>",
        views.transfer_outcoming,
        name="transfer_outcoming",
    ),
]

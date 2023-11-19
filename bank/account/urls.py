from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("create/", views.create_account, name="create"),
    path("list/", views.account_list, name="account_list"),
    path("detail/<int:account_id>/", views.account_detail, name="account_detail"),
    path("detail/<int:account_id>/edit/", views.edit_account, name="edit_account"),
    path("card/create/<int:account_id>", views.card_create, name="card_create"),
    path("card/list/", views.card_list, name="card_list"),
    path("card/detail/<int:card_id>/", views.card_detail, name="card_detail"),
    path("card/detail/<int:card_id>/edit", views.edit_card, name="edit_card"),
    path("status/<int:card_id>", views.change_status_card, name="status"),
    path(
        "delete/account/<int:account_id>", views.disable_account, name="disable_account"
    ),
    path("delete/card/<int:card_id>", views.cancel_card, name="cancel_card"),
]

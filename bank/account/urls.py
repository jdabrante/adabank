from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('create/', views.create_account, name='create'),
    path('list/', views.account_list, name='account_list'),
    path('detail/<int:account_id>/', views.account_detail, name='account_detail'),
    path('detail/<int:account_id>/edit/', views.edit_account, name='edit_account'),
    path('card/create/<int:account_id>', views.card_create, name='card_create'),
    path('card/list/', views.card_list, name='card_list'),
    path('card/detail/<int:card_id>/', views.card_detail, name='card_detail'),
    path('card/detail/<int:card_id>/edit', views.edit_card, name='edit_card'),
    path('status/<int:card_id>', views.change_status_card, name='status'),
    path(
        'delete/confirmation/<int:account_id>/',
        views.delete_account_confirmation,
        name='delete_confirmation',
    ),
    path('delete/account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('create/account/', views.create_account_confirmation, name='create_account_confirmation'),
    path('delete/card/<int:card_id>/', views.delete_card, name='delete_card'),
    path('transactions/', views.transaction_list, name='transaction_list'),
]

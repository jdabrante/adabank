from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('accounts/', views.AccountListView.as_view(), name='api_ccount_list'),
    path('accounts/<pk>/', views.AccountDetailView.as_view(), name='api_ccount_detail'),
    path('transactions/', views.TransactionListView.as_view(), name='api_transaction_list'),
    path('transactions/<pk>/', views.TransactionDetailView.as_view(), name='api_transaction_detail'),
    path('cards/',views.CardListView.as_view(), name='api_card_list' ),
    path('cards/<pk>/', views.CardDetailtView.as_view(), name='api_card_detail'),

]

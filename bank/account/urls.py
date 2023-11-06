from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [ 
    path('create/', views.create_account, name='create'),
    path('list/', views.account_list, name='account_list'),
    path('detail/<int:account_id>/', views.account_detail, name='account_detail'),
    path('card/create/', views.card_create, name='card_create')
]

from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'api'

router = routers.DefaultRouter()
router.register('accounts', views.AccountViewSet, basename='accounts')
router.register('cards', views.CardViewSet, basename='cards')
router.register('transactions', views.TransactionViewSet, basename='transactions')


urlpatterns = [
    path('', include(router.urls)),
]

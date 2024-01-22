from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('accounts/', views.AccountListView.as_view(), name='api_ccount_list'),
]

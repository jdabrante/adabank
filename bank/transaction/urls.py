from django.urls import path

from . import views

app_name = 'adabank'

urlpatterns = [
    path(
        'outcoming/<int:account_id>',
        views.transfer_outcoming,
        name='transfer_outcoming',
    ),
    path(
        'pdf/<int:transaction_id>',
        views.transaction_pdf,
        name='transaction_pdf',
    ),
    path(
        'outcoming_done/<int:transaction_id>',
        views.outcoming_done,
        name='outcoming_done',
    ),
    path('csv/<str:account_id>/', views.transactions_to_csv, name='transaction_to_csv'),
]

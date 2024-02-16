from django.urls import path

from . import views

app_name = 'adabank'

urlpatterns = [
    path('incoming/', views.transfer_incoming, name='transfer_incoming'),
    path(
        'outcoming/<int:account_id>',
        views.transfer_outcoming,
        name='transfer_outcoming',
    ),
    path('outcoming_all/', views.transfer_outcoming_all, name='transfer_outcoming_all'),
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

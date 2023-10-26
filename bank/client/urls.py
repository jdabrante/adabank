from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path(
        'passowrd-change/done',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
]

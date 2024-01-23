from rest_framework import generics

from account.models import Account

from .serializers import AccountSerializer


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

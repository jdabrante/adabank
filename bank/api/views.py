from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Account, Card
from transaction.models import Transaction

from .serializers import AccountSerializer, CardSerializer, TransactionSerializer


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset().filter(client__id=request.user.id)
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().filter(client__id=request.user.id)
        account = get_object_or_404(queryset, pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset().filter(account__client__id=request.user.id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().filter(account__client__id=request.user.id)
        card = get_object_or_404(queryset, pk=pk)
        serializer = CardSerializer(card)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset().filter(account__client__id=request.user.id)
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset().filter(account__client__id=request.user.id)
        transaction = get_object_or_404(queryset, pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

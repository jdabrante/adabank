from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models import Account, Card
from transaction.models import Transaction
from rest_framework.response import Response
from .serializers import AccountSerializer, TransactionSerializer, CardSerializer


class AccountListView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    def get(self, request):
        queryset = self.get_queryset().filter(client__username=request.user.username)
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)
    
class AccountDetailView(generics.RetrieveAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    # Check this...
    def get(self, request, pk):
        queryset = self.get_queryset().filter(client__username=request.user.username, code=pk)
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)
    
class TransactionListView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    def get(self, request):
        queryset = self.get_queryset().filter(account__client__username=request.user.username)
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

class TransactionDetailView(generics.RetrieveAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    #Check this...
    def get(self, request, pk):
        queryset = self.get_queryset().filter(account__client__username=request.user.username, pk=pk)
        serializer = AccountSerializer(queryset, many=True)
        return Response(serializer.data)

class CardListView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    def get(self, request):
        queryset = self.get_queryset().filter(account__client__username=request.user.username)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
    

class CardDetailtView(generics.RetrieveAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    def get(self, request, pk):
        queryset = self.get_queryset().filter(account__client__username=request.user.username, code=pk)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
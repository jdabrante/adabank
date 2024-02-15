from rest_framework import serializers

from account.models import Account, Card
from transaction.models import Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['client', 'code', 'alias', 'status', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['agent', 'concept', 'timestamp', 'amount', 'kind', 'account', 'card', 'commission']

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['account', 'code', 'alias', 'status', 'expiry']


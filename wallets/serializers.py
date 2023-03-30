from rest_framework import serializers
from .models import Wallets, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallets
        fields = ['id', 'currency', 'amount', 'user_id']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'amount', 'transaction_type', 'created_at']

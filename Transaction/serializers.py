from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'transaction_id',
            'account',
            'transaction_type',
            'amount',
            'balance_after_transaction',
            'created_at',
            'transaction_date',
            'status',
            'initiated_by',
            'fees',
        ]
        read_only_fields = ['id', 'created_at', 'transaction_id']  

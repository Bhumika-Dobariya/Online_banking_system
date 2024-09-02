from rest_framework import serializers
from .models import Transaction
import datetime
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'customer', 'account', 'source_account', 'destination_account', 'transaction_type', 'amount', 'balance_after_transaction', 'transaction_date', 'status', 'fees', 'created_at']
    
    
def is_valid_date(date_string):
    """Check if the date_string is in YYYY-MM-DD format."""
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
from rest_framework import serializers
from .models import BillPayment

class BillPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillPayment
        fields = ['id', 'customer', 'payment_type', 'amount', 'due_date', 'payment_date', 'status', 'payment_method']

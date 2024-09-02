from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        
    def validate_balance(self, value):
        if value < 500:
            raise serializers.ValidationError("The minimum balance must be 500.")
        return value
    
    def validate_account_number(self, value):
        if Account.objects.filter(account_number=value).exists():
            raise serializers.ValidationError("An account with this account number already exists.")
        return value

    def validate(self, data):
        account_type = data.get('account_type')
        if account_type not in dict(Account.ACCOUNT_TYPES).keys():
            raise serializers.ValidationError("Invalid account type.")
        
        return data
class AccountBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_number', 'account_type', 'business_or_personal', 'balance']

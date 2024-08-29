from rest_framework import serializers
from .models import CustomerSupport

class CustomerSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSupport
        fields = '__all__'  

 
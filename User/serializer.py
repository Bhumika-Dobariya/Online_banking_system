from rest_framework import serializers
from .models import User
from rest_framework import serializers
from django.contrib import admin
from .models import OTP
from uuid import UUID


from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'uname',
            'password',
            'role',
            'phone_number',
            'address',
            'date_of_birth',
            'is_active',
            'is_deleted',
            'is_verified',
            'created_at',
            'updated_at',
        ]
        
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
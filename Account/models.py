from django.db import models
from django.contrib.auth.models import User
import uuid

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('checking', 'Checking'),
        ('credit', 'Credit'),
    )
    
    ACCOUNT_CATEGORIES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='accounts', null=True, blank=True)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    business_or_personal = models.CharField(max_length=10, choices=ACCOUNT_CATEGORIES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.account_type} ({self.business_or_personal}) - {self.user.username}"


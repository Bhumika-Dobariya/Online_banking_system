from django.db import models
from django.utils import timezone
import uuid

class Investment(models.Model):
    INVESTMENT_TYPE_CHOICES = [
        ('fixed_deposit', 'Fixed Deposit'),
        ('mutual_fund', 'Mutual Fund'),
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('real_estate', 'Real Estate'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='investments')
    investment_type = models.CharField(max_length=50, choices=INVESTMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES)
    start_date = models.DateTimeField(default=timezone.now)
    maturity_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    return_on_investment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer}'s {self.investment_type} investment"

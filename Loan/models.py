from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Loan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed'),
        ('defaulted', 'Defaulted'),
    ]

    LOAN_TYPE_CHOICES = [
        ('personal', 'Personal Loan'),
        ('home', 'Home Loan'),
        ('auto', 'Auto Loan'),
        ('education', 'Education Loan'),
        ('business', 'Business Loan'),
        ('gold', 'Gold Loan'),
    ]

    INTEREST_RATES = {
        'personal': 12.0,
        'home': 8.0,
        'auto': 10.0,
        'education': 7.0,
        'business': 14.0,
        'gold': 6.0,
    }

    PROCESSING_FEES = {
        'personal': 0.01,  # 1% of loan amount
        'home': 0.005,     # 0.5% of loan amount
        'auto': 0.01,      # 1% of loan amount
        'education': 0.007, # 0.7% of loan amount
        'business': 0.015, # 1.5% of loan amount
        'gold': 0.003,     # 0.3% of loan amount
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_months = models.IntegerField()
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    applied_date = models.DateTimeField(default=timezone.now)
    approved_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=12, choices=LOAN_STATUS_CHOICES, default='pending')
    collateral_details = models.TextField(blank=True, null=True)
    overdue_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0.00)
    last_payment_date = models.DateTimeField(blank=True, null=True)
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.loan_type} Loan - {self.customer}"

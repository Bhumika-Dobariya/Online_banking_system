from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class Offer(models.Model):
    OFFER_TYPES = (
        ('cashback', 'Cashback'),
        ('interest_discount', 'Interest Rate Discount'),
        ('fee_waiver', 'Fee Waiver'),
        ('reward_points', 'Reward Points'),
        ('signup_bonus', 'Signup Bonus'),
        ('transaction_bonus', 'Transaction Bonus'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('upcoming', 'Upcoming'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title  = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Value of the offer (e.g., cashback amount, interest discount rate).")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    applicable_to = models.CharField(max_length=100, help_text="Applicable to products like 'Credit Card', 'Savings Account', 'Loan', etc.")

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    def is_valid(self):
        """
        Check if the offer is currently valid based on the start and end dates.
        """
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active

    def apply_offer(self, original_value):
        """
        Apply the offer to the original value (e.g., transaction amount, interest rate).
        """
        if self.offer_type == 'cashback':
            return original_value - self.value
        elif self.offer_type == 'interest_discount':
            return original_value * (1 - self.value / 100)
        elif self.offer_type == 'fee_waiver':
            return 0  
        elif self.offer_type == 'reward_points':
            return original_value  
        elif self.offer_type == 'signup_bonus':
            return original_value + self.value  
        elif self.offer_type == 'transaction_bonus':
            return original_value + self.value  
        return original_value

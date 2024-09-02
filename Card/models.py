from django.db import models
from django.utils import timezone
import uuid


class Card(models.Model):
    
    CARD_TYPE_CHOICES = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
    ]

    CARD_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
        ('expired', 'Expired'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='cards')
    linked_account = models.ForeignKey('Account.Account', on_delete=models.CASCADE, related_name='cards')  
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES)
    cardholder_name = models.CharField(max_length=255)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)
    bank_name = models.CharField(max_length=255)
    issue_date = models.DateField()
    pin = models.CharField(max_length=4)  
    daily_transaction_limit = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)  
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    status = models.CharField(max_length=10, choices=CARD_STATUS_CHOICES, default='active')  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.card_type.capitalize()} Card - {self.card_number[-4:]}"

    def save(self, *args, **kwargs):
        if self.bill:
            self.payment_type = self.bill.bill_type

            # Validate if the card belongs to the customer associated with the bill
            if self.payment_method and self.bill.customer != self.payment_method.customer:
                raise ValueError("The payment method does not belong to the customer associated with the bill.")

            # Deduct the amount from the card's balance if the status is "completed"
            if self.status == 'completed':
                card = self.payment_method
                if card.balance >= self.amount:
                    card.balance -= self.amount
                    card.save()
                else:
                    raise ValueError("Insufficient balance on the card to complete the payment.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.payment_type} - {self.bill.customer} - {self.amount} paid on {self.payment_date if self.payment_date else 'Not Paid Yet'}"

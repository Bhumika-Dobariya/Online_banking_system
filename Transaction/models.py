from django.db import models
import uuid
from django.utils import timezone

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    ]

    TRANSACTION_STATUSES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey('Account.Account', on_delete=models.CASCADE, related_name='transactions')
    source_account = models.ForeignKey('Account.Account', related_name='source_transactions', on_delete=models.CASCADE, null=True, blank=True)
    destination_account = models.ForeignKey('Account.Account', related_name='destination_transactions', on_delete=models.CASCADE, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUSES, default='Pending')
    fees = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_number} - {self.transaction_id}"

    class Meta:
        ordering = ['-created_at']  

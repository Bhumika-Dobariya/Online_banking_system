from django.db import models
import uuid

class Bill(models.Model):
    BILL_TYPES = (
        ('Electricity', 'Electricity'),
        ('Water', 'Water'),
        ('Internet', 'Internet'),
        ('Phone', 'Phone'),
        ('Other', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='bills')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPES)

    def __str__(self):
        return f"Bill for {self.customer} - {self.amount_due} due on {self.due_date}"




class BillPayment(models.Model):
    PAYMENT_TYPES = (
        ('Electricity', 'Electricity'),
        ('Water', 'Water'),
        ('Internet', 'Internet'),
        ('Phone', 'Phone'),
        ('Other', 'Other'),
    )
    
    PAYMENT_METHODS = (
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
        ('Online Payment', 'Online Payment'),
        ('Other', 'Other'),
    )
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='billpayments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, null=True, blank=True) 
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.payment_type} - {self.bill.customer} - {self.amount} paid on {self.payment_date if self.payment_date else 'Not Paid Yet'}"

from django.db import models
import uuid

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
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, null=True, blank=True) 

    def __str__(self):
        return f"{self.payment_type} - {self.customer.user.username}"


from django.db import models

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
    billing_address = models.TextField()  
    daily_transaction_limit = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00)  
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    status = models.CharField(max_length=10, choices=CARD_STATUS_CHOICES, default='active')  

    def __str__(self):
        return f"{self.card_type.capitalize()} Card - {self.card_number[-4:]}"

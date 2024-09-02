from django.db import models
import uuid
from decimal import Decimal

class Investment(models.Model):
    INVESTMENT_TYPE_CHOICES = [
        ('fixed_deposit', 'Fixed Deposit'),
        ('mutual_fund', 'Mutual Fund'),
        ('stock', 'Stock'),
        ('bond', 'Bond'),
        ('real_estate', 'Real Estate'),
    ]
    
    # Define rates for each type
    INVESTMENT_RATES = {
        'fixed_deposit': 10.0, 
        'mutual_fund': 8.0,     
        'stock': 12.0,        
        'bond': 7.0,           
        'real_estate': 6.0,    
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='Investments', null=True, blank=True)
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    investment_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  
    total_profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if self.investment_type in self.INVESTMENT_RATES:
            self.investment_rate = Decimal(self.INVESTMENT_RATES[self.investment_type])
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.investment_type} - {self.amount}"

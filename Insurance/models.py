from django.db import models
import uuid

class Insurance(models.Model):
    POLICY_TYPES = [
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
        ('vehicle', 'Vehicle Insurance'),
        ('home', 'Home Insurance'),
        ('travel', 'Travel Insurance'),  
    ]
    
    DEFAULT_COVERAGE_AMOUNTS = {
        'health': 100000.00,
        'life': 500000.00,
        'vehicle': 1000000.00,
        'home': 5000000.00,
        'travel': 500000.00,
    }
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='Insurance', null=True, blank=True)
    policy_number = models.CharField(max_length=50, unique=True) 
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)  
    provider_name = models.CharField(max_length=100) 
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)  
    terms_conditions = models.TextField(blank=True, null=True) 
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    start_date = models.DateField()  
    end_date = models.DateField() 
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if not self.coverage_amount and self.policy_type in self.DEFAULT_COVERAGE_AMOUNTS:
            self.coverage_amount = self.DEFAULT_COVERAGE_AMOUNTS[self.policy_type]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.policy_number} - {self.policy_type}"

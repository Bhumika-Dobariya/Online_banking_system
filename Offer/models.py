from django.db import models
from django.utils import timezone
import uuid

class Offer(models.Model):
    OFFER_TYPES = (
        ('discount', 'Discount'),
        ('cashback', 'Cashback'),
        ('buy_one_get_one', 'Buy One Get One'),
        ('free_trial', 'Free Trial'),
        ('other', 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    cashback_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField()
    applicable_to = models.CharField(max_length=50)  
    entity_id = models.UUIDField()  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_until


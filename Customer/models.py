from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError

class Customer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='customer')
    email = models.EmailField(unique=True, blank=False)
    uname = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.uname

    def save(self, *args, **kwargs):
        if self.user:
            if self.user.role != 'Customer':
                raise ValidationError("Only users with the role 'Customer' can be associated with the Customer model.")
            self.email = self.user.email
            self.name = self.user.uname
        super().save(*args, **kwargs)

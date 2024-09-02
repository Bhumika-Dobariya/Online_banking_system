from django.db import models
import uuid

class Branch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    branch_code = models.CharField(max_length=20, unique=True)  
    manager_name = models.CharField(max_length=100, blank=True, null=True) 
    operating_hours = models.CharField(max_length=100, blank=True, null=True) 
    status = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

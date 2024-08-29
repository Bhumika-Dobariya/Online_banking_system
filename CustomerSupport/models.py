from django.db import models
import uuid

class CustomerSupport(models.Model):
    REQUEST_TYPES = (
        ('inquiry', 'Inquiry'),
        ('complaint', 'Complaint'),
        ('technical_support', 'Technical Support'),
        ('account_issue', 'Account Issue'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE, related_name='support_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"

    

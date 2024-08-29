from django.db import models
import uuid


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Info', 'Info'),
        ('Warning', 'Warning'),
        ('Alert', 'Alert'),
        ('Promotion', 'Promotion'),
        ('Reminder', 'Reminder'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer.Customer', on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='Info')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.customer} - {self.notification_type}"

  

from django.urls import path
from .views import (
    create_notification,
    get_notification_by_id,
    get_all_notifications,
    update_notification,
    delete_notification,
    get_notifications_by_type,
    get_notifications_by_customer,
    get_notifications_by_read_status,
)

urlpatterns = [
    path('create/', create_notification, name='create_notification'),
    path('get/', get_notification_by_id, name='get_notification_by_id'),
    path('list/', get_all_notifications, name='get_all_notifications'),
    path('update/', update_notification, name='update_notification'),
    path('delete/', delete_notification, name='delete_notification'),
    path('type/', get_notifications_by_type, name='get_notifications_by_type'),
    path('customer/', get_notifications_by_customer, name='get_notifications_by_customer'),
    path('status/', get_notifications_by_read_status, name='get_notifications_by_read_status'),
]

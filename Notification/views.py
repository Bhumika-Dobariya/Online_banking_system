from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

# _____________ Create Notification _____________

@api_view(["POST"])
def create_notification(request):
    serializer = NotificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Notification by ID _____________

@api_view(["GET"])
def get_notification_by_id(request):
    notification_id = request.query_params.get('id')
    if not notification_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    notification = Notification.objects.filter(id=notification_id).first()
    if notification:
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get All Notifications _____________

@api_view(["GET"])
def get_all_notifications(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Notification _____________

@api_view(["PUT"])
def update_notification(request):
    notification_id = request.query_params.get('id')
    if not notification_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    notification = Notification.objects.filter(id=notification_id).first()
    if notification:
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Delete Notification (Mark as Read) _____________

@api_view(["DELETE"])
def delete_notification(request):
    notification_id = request.query_params.get('id')
    if not notification_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    notification = Notification.objects.filter(id=notification_id).first()
    if notification:
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Notifications by Type _____________

@api_view(["GET"])
def get_notifications_by_type(request):
    notification_type = request.query_params.get('type')
    if not notification_type:
        return Response({"detail": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    notifications = Notification.objects.filter(notification_type=notification_type)
    if notifications.exists():
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No notifications found for the specified type"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Notifications by Customer _____________

@api_view(["GET"])
def get_notifications_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    notifications = Notification.objects.filter(customer_id=customer_id)
    if notifications.exists():
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No notifications found for the specified customer"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Notifications by Read Status _____________

@api_view(["GET"])
def get_notifications_by_read_status(request):
    is_read = request.query_params.get('is_read')
    if is_read not in ['true', 'false']:
        return Response({"detail": "is_read parameter must be 'true' or 'false'"}, status=status.HTTP_400_BAD_REQUEST)

    is_read = is_read == 'true'
    notifications = Notification.objects.filter(is_read=is_read)
    if notifications.exists():
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No notifications found for the specified read status"}, status=status.HTTP_404_NOT_FOUND)


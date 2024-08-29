from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomerSupport
from .serializers import CustomerSupportSerializer

# _____________ Create Support Request _____________

@api_view(["POST"])
def create_support_request(request):
    serializer = CustomerSupportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Support Request by ID _____________

@api_view(["GET"])
def get_support_request_by_id(request):
    support_id = request.query_params.get('id')
    if not support_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_request = CustomerSupport.objects.filter(id=support_id).first()
    if support_request:
        serializer = CustomerSupportSerializer(support_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Support request not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get All Support Requests _____________

@api_view(["GET"])
def get_all_support_requests(request):
    support_requests = CustomerSupport.objects.all()
    serializer = CustomerSupportSerializer(support_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Support Request _____________

@api_view(["PUT"])
def update_support_request(request):
    support_id = request.query_params.get('id')
    if not support_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_request = CustomerSupport.objects.filter(id=support_id).first()
    if support_request:
        serializer = CustomerSupportSerializer(support_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Support request not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Delete Support Request _____________

@api_view(["DELETE"])
def delete_support_request(request):
    support_id = request.query_params.get('id')
    if not support_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_request = CustomerSupport.objects.filter(id=support_id).first()
    if support_request:
        support_request.delete()
        return Response({"detail": "Support request deleted"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Support request not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Support Requests by Status _____________

@api_view(["GET"])
def get_support_requests_by_status(request):
    status_filter = request.query_params.get('status')
    if not status_filter:
        return Response({"detail": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_requests = CustomerSupport.objects.filter(status=status_filter)
    serializer = CustomerSupportSerializer(support_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Get Support Requests by Customer _____________

@api_view(["GET"])
def get_support_requests_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_requests = CustomerSupport.objects.filter(customer_id=customer_id)
    serializer = CustomerSupportSerializer(support_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Close/Resolve Support Request _____________

@api_view(["PATCH"])
def close_support_request(request):
    support_id = request.query_params.get('id')
    if not support_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_request = CustomerSupport.objects.filter(id=support_id).first()
    if support_request:
        serializer = CustomerSupportSerializer(support_request, data={"status": "Resolved"}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Support request not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Search Support Requests _____________

@api_view(["GET"])
def search_support_requests(request):
    query = request.query_params.get('query')
    if not query:
        return Response({"detail": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    support_requests = CustomerSupport.objects.filter(description__icontains=query)
    serializer = CustomerSupportSerializer(support_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

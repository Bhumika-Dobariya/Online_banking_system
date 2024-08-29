from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer


@api_view(["POST"])
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_customer_by_id(request):
    customer_id = request.query_params.get('id')
    if not customer_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    customer = Customer.objects.filter(id=customer_id, is_deleted=False, is_active=True).first()
    if customer:
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Customer not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_all_customers(request):
    customers = Customer.objects.filter(is_deleted=False, is_active=True)
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["PUT"])
def update_customer(request):
    customer_id = request.query_params.get('id')
    if not customer_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    customer = Customer.objects.filter(id=customer_id, is_deleted=False, is_active=True).first()
    if customer:
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Customer not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_customer(request):
    customer_id = request.query_params.get('id')
    if not customer_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    customer = Customer.objects.filter(id=customer_id, is_deleted=False, is_active=True).first()
    if customer:
        customer.is_deleted = True
        customer.is_active = False
        customer.save()
        return Response({"detail": "Customer marked as deleted and deactivated"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Customer not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)



# _____________ Get Customers by Gender _____________

@api_view(["GET"])
def get_customers_by_gender(request):
    gender = request.query_params.get('gender')
    if not gender:
        return Response({"detail": "Gender parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    customers = Customer.objects.filter(gender=gender, is_deleted=False, is_active=True)
    if customers.exists():
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No customers found for the specified gender or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Customers by Name _____________

@api_view(["GET"])
def get_customers_by_name(request):
    name = request.query_params.get('name')
    if not name:
        return Response({"detail": "Name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    customers = Customer.objects.filter(name__icontains=name, is_deleted=False, is_active=True)
    if customers.exists():
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No customers found with the specified name or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)

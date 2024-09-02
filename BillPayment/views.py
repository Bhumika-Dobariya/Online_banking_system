from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BillPayment
from .serializers import BillPaymentSerializer
from datetime import datetime
from .models import Bill
from .serializers import BillSerializer


# _____________ Create Bill _____________

@api_view(["POST"])
def create_bill(request):
    serializer = BillSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Bill by ID _____________

@api_view(["GET"])
def get_bill_by_id(request):
    bill_id = request.query_params.get('id')
    if not bill_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill = Bill.objects.filter(id=bill_id).first()
    if bill:
        serializer = BillSerializer(bill)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get All Bills _____________

@api_view(["GET"])
def get_all_bills(request):
    bills = Bill.objects.all()
    serializer = BillSerializer(bills, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Bill _____________

@api_view(["PUT"])
def update_bill(request):
    bill_id = request.query_params.get('id')
    if not bill_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill = Bill.objects.filter(id=bill_id).first()
    if bill:
        serializer = BillSerializer(bill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Delete Bill _____________

@api_view(["DELETE"])
def delete_bill(request):
    bill_id = request.query_params.get('id')
    if not bill_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill = Bill.objects.filter(id=bill_id).first()
    if bill:
        bill.delete()
        return Response({"detail": "Bill deleted"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Bills by Customer ID _____________

@api_view(["GET"])
def get_bills_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bills = Bill.objects.filter(customer_id=customer_id)
    if bills.exists():
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No bills found for the specified customer"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Bills by Bill Type _____________

@api_view(["GET"])
def get_bills_by_bill_type(request):
    bill_type = request.query_params.get('bill_type')
    if not bill_type:
        return Response({"detail": "Bill type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bills = Bill.objects.filter(bill_type=bill_type)
    if bills.exists():
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No bills found for the specified bill type"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Bills by Due Date Range _____________

@api_view(["GET"])
def get_bills_by_due_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({"detail": "Both start_date and end_date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    bills = Bill.objects.filter(due_date__range=[start_date, end_date])
    if bills.exists():
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No bills found within the specified date range"}, status=status.HTTP_404_NOT_FOUND)



######################### Bill payment #####################################


# _____________ Create Bill Payment _____________

@api_view(["POST"])
def create_bill_payment(request):
    serializer = BillPaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Bill Payment by ID _____________

@api_view(["GET"])
def get_bill_payment_by_id(request):
    bill_payment_id = request.query_params.get('id')
    if not bill_payment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill_payment = BillPayment.objects.filter(id=bill_payment_id).first()
    if bill_payment:
        serializer = BillPaymentSerializer(bill_payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Bill payment not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get All Bill Payments _____________

@api_view(["GET"])
def get_all_bill_payments(request):
    bill_payments = BillPayment.objects.all()
    serializer = BillPaymentSerializer(bill_payments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Bill Payment _____________

@api_view(["PUT"])
def update_bill_payment(request):
    bill_payment_id = request.query_params.get('id')
    if not bill_payment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill_payment = BillPayment.objects.filter(id=bill_payment_id).first()
    if bill_payment:
        serializer = BillPaymentSerializer(bill_payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Bill payment not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Delete Bill Payment _____________

@api_view(["DELETE"])
def delete_bill_payment(request):
    bill_payment_id = request.query_params.get('id')
    if not bill_payment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill_payment = BillPayment.objects.filter(id=bill_payment_id).first()
    if bill_payment:
        bill_payment.delete()
        return Response({"detail": "Bill payment deleted"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Bill payment not found"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Bill Payments by Payment Type _____________

@api_view(["GET"])
def get_bill_payments_by_payment_type(request):
    payment_type = request.query_params.get('payment_type')
    if not payment_type:
        return Response({"detail": "Payment type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill_payments = BillPayment.objects.filter(payment_type=payment_type)
    if bill_payments.exists():
        serializer = BillPaymentSerializer(bill_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No bill payments found for the specified payment type"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Bill Payments by Due Date Range _____________

@api_view(["GET"])
def get_bill_payments_by_due_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({"detail": "Both start_date and end_date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    bill_payments = BillPayment.objects.filter(due_date__range=[start_date, end_date])
    if bill_payments.exists():
        serializer = BillPaymentSerializer(bill_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No bill payments found within the specified date range"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_bill_payments_by_payment_method(request):
    payment_method = request.query_params.get('payment_method')
    if not payment_method:
        return Response({"detail": "Payment method parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    bill_payments = BillPayment.objects.filter(payment_method=payment_method)
    if bill_payments.exists():
        serializer = BillPaymentSerializer(bill_payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No bill payments found with the specified payment method"}, status=status.HTTP_404_NOT_FOUND)
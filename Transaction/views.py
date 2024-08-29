from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer
from django.utils import timezone


@api_view(["POST"])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def get_transaction_by_id(request):
    transaction_id = request.query_params.get('id')
    if not transaction_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_all_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["PUT"])
def update_transaction(request):
    transaction_id = request.query_params.get('id')
    if not transaction_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["DELETE"])
def delete_transaction(request):
    transaction_id = request.query_params.get('id')
    if not transaction_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    transaction = Transaction.objects.filter(id=transaction_id).first()
    if transaction:
        transaction.delete()
        return Response({"detail": "Transaction deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_transactions_by_type(request):
    transaction_type = request.query_params.get('type')
    if not transaction_type:
        return Response({"detail": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if transaction_type not in dict(Transaction.TRANSACTION_TYPES).keys():
        return Response({"detail": "Invalid transaction type"}, status=status.HTTP_400_BAD_REQUEST)
    
    transactions = Transaction.objects.filter(transaction_type=transaction_type)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_transactions_by_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({"detail": "Start date and end date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        start_date = timezone.datetime.fromisoformat(start_date)
        end_date = timezone.datetime.fromisoformat(end_date)
    except ValueError:
        return Response({"detail": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(created_at__range=[start_date, end_date])
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_transactions_by_status(request):
    status_param = request.query_params.get('status')
    if not status_param:
        return Response({"detail": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if status_param not in dict(Transaction.TRANSACTION_STATUSES).keys():
        return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
    
    transactions = Transaction.objects.filter(status=status_param)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_transactions_by_account(request):
    account_id = request.query_params.get('account_id')
    if not account_id:
        return Response({"detail": "Account ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(account_id=account_id)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

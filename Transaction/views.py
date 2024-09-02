from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from Account.models import Account
from .serializers import TransactionSerializer,is_valid_date
from django.utils import timezone
import datetime
from decimal import Decimal  


FIXED_FEES = {
    'Deposit': Decimal('0.00'),
    'Withdrawal': Decimal('0.00'),
    'Transfer': Decimal('10.00')  
}

@api_view(["POST"])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    
    if serializer.is_valid():
        transaction = serializer.save()
        transaction_type = transaction.transaction_type

        if transaction_type == 'Deposit':
            account = Account.objects.get(pk=transaction.account.id)
            account.balance += transaction.amount
            account.save()
            transaction.balance_after_transaction = account.balance
        
        elif transaction_type == 'Withdrawal':
            account = Account.objects.get(pk=transaction.account.id)
            if account.balance >= transaction.amount:
                account.balance -= transaction.amount
                account.save()
                transaction.balance_after_transaction = account.balance
            else:
                return Response({"detail": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif transaction_type == 'Transfer':
            source_account = Account.objects.get(pk=transaction.source_account.id)
            destination_account = Account.objects.get(pk=transaction.destination_account.id)
            
            fee = FIXED_FEES.get(transaction_type, Decimal('0.00'))
            if source_account.balance >= (transaction.amount + fee):
                source_account.balance -= (transaction.amount + fee)
                destination_account.balance += transaction.amount
                
                source_account.save()
                destination_account.save()

                transaction.balance_after_transaction = source_account.balance
                transaction.fees = fee
            else:
                return Response({"detail": "Insufficient funds in source account"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.save()
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
    transaction_type = request.query_params.get('  ')
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

    if not (is_valid_date(start_date) and is_valid_date(end_date)):
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)

    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    transactions = Transaction.objects.filter(created_at__date__range=[start_date, end_date])
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


@api_view(["GET"])
def get_transactions_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(customer_id=customer_id)
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_transactions_by_amount_range(request):
    min_amount = request.query_params.get('min_amount')
    max_amount = request.query_params.get('max_amount')

    if not min_amount or not max_amount:
        return Response({"detail": "Min amount and max amount parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        min_amount = float(min_amount)
        max_amount = float(max_amount)
    except ValueError:
        return Response({"detail": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

    transactions = Transaction.objects.filter(amount__range=[min_amount, max_amount])
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

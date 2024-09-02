from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializer import AccountSerializer,AccountBasicSerializer
from decimal import Decimal, InvalidOperation


# _____________ Create Account ___________________

@api_view(["POST"])
def create_account(request):
    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Account by ID ___________________

@api_view(["GET"])
def get_account_by_id(request):
    account_id = request.query_params.get('id')
    if not account_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    account = get_object_or_404(Account, pk=account_id)
    serializer = AccountSerializer(account)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Get All Accounts ___________________

@api_view(["GET"])
def get_all_accounts(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Account ___________________

@api_view(["PUT"])
def update_account(request):
    account_id = request.query_params.get('id')
    if not account_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    account = get_object_or_404(Account, pk=account_id)
    serializer = AccountSerializer(account, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Delete Account ___________________

@api_view(["DELETE"])
def delete_account(request):
    account_id = request.query_params.get('id')
    if not account_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    account = get_object_or_404(Account, pk=account_id)
    account.delete()
    return Response({"detail": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# _____________ Get Accounts by Type ___________________

@api_view(["GET"])
def get_accounts_by_type(request):
    account_type = request.query_params.get('account_type')
    if account_type:
        accounts = Account.objects.filter(account_type=account_type)
    else:
        accounts = Account.objects.all()
    
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# _____________ Get Accounts by User ___________________

@api_view(["GET"])
def get_accounts_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    accounts = Account.objects.filter(customer_id=customer_id)
    if accounts.exists():
        serializer = AccountBasicSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "No accounts found for the given customer ID"}, status=status.HTTP_404_NOT_FOUND)



# _____________ Activate/Deactivate Account ___________________


@api_view(["PATCH"])
def toggle_account_status(request):
    account_id = request.query_params.get('id')
    if not account_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    account = Account.objects.filter(pk=account_id).first()
    if not account:
        return Response({"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND)
    
    account.is_active = not account.is_active
    account.save()
    
    if account.is_active:
        status_msg = "activated"
    else:
        status_msg = "deactivated"
    
    return Response({"detail": f"Account {status_msg} successfully"}, status=status.HTTP_200_OK)


# _____________ Filter Accounts by Balance Range ___________________

@api_view(["GET"])
def filter_accounts_by_balance(request):
    min_balance = request.query_params.get('min_balance')
    max_balance = request.query_params.get('max_balance')

    filters = {}
    try:
        if min_balance is not None:
            min_balance = Decimal(min_balance)
            if min_balance < 0:
                return Response({"detail": "Minimum balance must be non-negative"}, status=status.HTTP_400_BAD_REQUEST)
            filters['balance__gte'] = min_balance

        if max_balance is not None:
            max_balance = Decimal(max_balance)
            if max_balance < 0:
                return Response({"detail": "Maximum balance must be non-negative"}, status=status.HTTP_400_BAD_REQUEST)
            filters['balance__lte'] = max_balance

        if 'balance__gte' in filters and 'balance__lte' in filters and filters['balance__gte'] > filters['balance__lte']:
            return Response({"detail": "Minimum balance cannot be greater than maximum balance"}, status=status.HTTP_400_BAD_REQUEST)

    except (ValueError, InvalidOperation):
        return Response({"detail": "Invalid balance value"}, status=status.HTTP_400_BAD_REQUEST)

    accounts = Account.objects.filter(**filters)
    serializer = AccountBasicSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




# _____________ Transfer Funds Between Accounts ___________________

@api_view(["POST"])
def transfer_funds(request):
    from_account_id = request.query_params.get('from_account_id')
    to_account_id = request.query_params.get('to_account_id')
    amount = request.query_params.get('amount')

    if not from_account_id or not to_account_id or not amount:
        return Response({"detail": "From account ID, to account ID, and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
    except (ValueError, InvalidOperation):
        return Response({"detail": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

    from_account = Account.objects.filter(pk=from_account_id).first()
    to_account = Account.objects.filter(pk=to_account_id).first()

    if not from_account:
        return Response({"detail": "From account not found"}, status=status.HTTP_404_NOT_FOUND)
    if not to_account:
        return Response({"detail": "To account not found"}, status=status.HTTP_404_NOT_FOUND)

    if from_account.balance < amount:
        return Response({"detail": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

    MIN_BALANCE = Decimal('500.00')
    if from_account.balance - amount < MIN_BALANCE:
        return Response({"detail": f"Insufficient funds to maintain minimum balance of {MIN_BALANCE}"}, status=status.HTTP_400_BAD_REQUEST)

    from_account.balance -= amount
    to_account.balance += amount

    from_account.save()
    to_account.save()

    return Response({"detail": "Funds transferred successfully"}, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_personal_accounts(request):
    accounts = Account.objects.filter(business_or_personal='personal', is_active=True)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

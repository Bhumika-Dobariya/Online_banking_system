from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializer import AccountSerializer

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
def get_accounts_by_user(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({"detail": "User ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    accounts = Account.objects.filter(user_id=user_id)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Activate/Deactivate Account ___________________

@api_view(["PATCH"])
def toggle_account_status(request):
    account_id = request.query_params.get('id')
    if not account_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    account = get_object_or_404(Account, pk=account_id)
    account.is_active = not account.is_active
    account.save()
    status_msg = "activated" if account.is_active else "deactivated"
    return Response({"detail": f"Account {status_msg} successfully"}, status=status.HTTP_200_OK)

# _____________ Filter Accounts by Balance Range ___________________

@api_view(["GET"])
def filter_accounts_by_balance(request):
    min_balance = request.query_params.get('min_balance')
    max_balance = request.query_params.get('max_balance')

    filters = {}
    if min_balance is not None:
        filters['balance__gte'] = min_balance
    if max_balance is not None:
        filters['balance__lte'] = max_balance

    accounts = Account.objects.filter(**filters)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Transfer Funds Between Accounts ___________________

@api_view(["POST"])
def transfer_funds(request):
    from_account_id = request.data.get('from_account_id')
    to_account_id = request.data.get('to_account_id')
    amount = request.data.get('amount')

    if not from_account_id or not to_account_id or not amount:
        return Response({"detail": "From account ID, to account ID, and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

    from_account = get_object_or_404(Account, pk=from_account_id)
    to_account = get_object_or_404(Account, pk=to_account_id)

    if from_account.balance < amount:
        return Response({"detail": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

    from_account.balance -= amount
    to_account.balance += amount

    from_account.save()
    to_account.save()

    return Response({"detail": "Funds transferred successfully"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_accounts_by_balance_gt(request):
    min_balance = request.query_params.get('min_balance')
    if not min_balance:
        return Response({"detail": "min_balance query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    accounts = Account.objects.filter(balance__gt=min_balance)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_accounts_by_balance_gt(request):
    min_balance = request.query_params.get('min_balance')
    if not min_balance:
        return Response({"detail": "min_balance query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    accounts = Account.objects.filter(balance__gt=min_balance)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


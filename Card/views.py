from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Card
from .serializers import CardSerializer
from datetime import datetime, timedelta
from Transaction.serializers import TransactionSerializer
from decimal import Decimal


# _____________ Create Card ___________________


@api_view(["POST"])
def create_card(request):
    serializer = CardSerializer(data=request.data)
    
    if serializer.is_valid():
        card = serializer.save()
        card_type = card.card_type  

        if card_type == 'Credit':
            if not card.credit_limit:
                card.credit_limit = 5000.00
            if not card.transaction_limit:
                card.transaction_limit = 1000.00
            card.save()

        elif card_type == 'Debit':
            if not card.associated_account:
                return Response({"detail": "Associated account is required"}, status=status.HTTP_400_BAD_REQUEST)
            if not card.transaction_limit:
                card.transaction_limit = 500.00
            card.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# _____________ Get Card by ID ___________________

@api_view(["GET"])
def get_card_by_id(request):
    card_id = request.query_params.get('id')
    if not card_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    card = get_object_or_404(Card, pk=card_id)
    serializer = CardSerializer(card)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Get All Cards ___________________

@api_view(["GET"])
def get_all_cards(request):
    cards = Card.objects.all()
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Card ___________________

@api_view(["PUT"])
def update_card(request):
    card_id = request.query_params.get('id')
    if not card_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    card = get_object_or_404(Card, pk=card_id)
    serializer = CardSerializer(card, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Delete Card ___________________

@api_view(["DELETE"])
def delete_card(request):
    card_id = request.query_params.get('id')
    if not card_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    card = get_object_or_404(Card, pk=card_id)
    card.delete()
    return Response({"detail": "Card deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# _____________ Get Cards by Type ___________________

@api_view(["GET"])
def get_cards_by_type(request):
    card_type = request.query_params.get('card_type')
    if card_type:
        cards = Card.objects.filter(card_type=card_type)
    else:
        cards = Card.objects.all()
    
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Get Cards by Customer ___________________

@api_view(["GET"])
def get_cards_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    cards = Card.objects.filter(customer_id=customer_id)
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# _____________ Filter Cards by Balance Range ___________________

@api_view(["GET"])
def filter_cards_by_balance(request):
    min_balance = request.query_params.get('min_balance')
    max_balance = request.query_params.get('max_balance')

    filters = {}
    if min_balance is not None:
        filters['available_balance__gte'] = min_balance
    if max_balance is not None:
        filters['available_balance__lte'] = max_balance

    cards = Card.objects.filter(**filters)
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# _____________ Transfer Funds Between Cards ___________________

@api_view(["POST"])
def transfer_funds_between_cards(request):

    from_card_number = request.query_params.get('from_card_number')
    to_card_number = request.query_params.get('to_card_number')
    amount = request.query_params.get('amount')

    if not from_card_number or not to_card_number or amount is None:
        return Response({"detail": "From card number, to card number, and amount are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = Decimal(amount)  
        if amount <= 0:
            return Response({"detail": "Amount must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({"detail": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

    from_card = Card.objects.filter(card_number=from_card_number).first()
    to_card = Card.objects.filter(card_number=to_card_number).first()

    if from_card is None:
        return Response({"detail": "From card not found"}, status=status.HTTP_404_NOT_FOUND)
    if to_card is None:
        return Response({"detail": "To card not found"}, status=status.HTTP_404_NOT_FOUND)

    if from_card.available_balance < amount:
        return Response({"detail": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)

    from_card.available_balance -= amount
    to_card.available_balance += amount

    from_card.save()
    to_card.save()

    return Response({"detail": "Funds transferred successfully"}, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def deactivate_card(request):
    card_id = request.query_params.get('id')
    if not card_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    card_exists = Card.objects.filter(pk=card_id).exists()
    if not card_exists:
        return Response({"detail": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
    
    card = Card.objects.get(pk=card_id)

    card.status = 'inactive'
    card.save()
    
    return Response({"detail": "Card deactivated successfully"}, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def reactivate_card(request):
    card_id = request.query_params.get('id')
    if not card_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    card = get_object_or_404(Card, pk=card_id)
    card.status = 'active'
    card.save()
    return Response({"detail": "Card reactivated successfully"}, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_expiring_cards(request):
    days_until_expiry = request.query_params.get('days_until_expiry', 30)  
    try:
        days_until_expiry = int(days_until_expiry)
    except ValueError:
        return Response({"detail": "Invalid number of days"}, status=status.HTTP_400_BAD_REQUEST)
    
    expiry_threshold = datetime.now().date() + timedelta(days=days_until_expiry)
    cards = Card.objects.filter(expiration_date__lte=expiry_threshold)
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["PATCH"])
def update_card_pin(request):
    card_id = request.query_params.get('id')
    new_pin = request.data.get('pin')
    
    if not card_id or not new_pin:
        return Response({"detail": "ID and new PIN are required"}, status=status.HTTP_400_BAD_REQUEST)

    card_exists = Card.objects.filter(pk=card_id).exists()
    if not card_exists:
        return Response({"detail": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
    
    card = Card.objects.get(pk=card_id)

    card.pin = new_pin
    card.save()
    
    return Response({"detail": "Card PIN updated successfully"}, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_cards_by_bank(request):
    bank_name = request.query_params.get('bank_name')
    if not bank_name:
        return Response({"detail": "Bank name query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    cards = Card.objects.filter(bank_name__icontains=bank_name)
    serializer = CardSerializer(cards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_card_with_transactions(request):
    card_id = request.query_params.get('id')
    if not card_id:
        return Response({"detail": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    card = Card.objects.filter(pk=card_id).first()
    if not card:
        return Response({"detail": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
    
    card_serializer = CardSerializer(card)
    
    transactions = card.transactions.all()
    transaction_serializer = TransactionSerializer(transactions, many=True)
    
    return Response({
        "card": card_serializer.data,
        "transactions": transaction_serializer.data
    }, status=status.HTTP_200_OK)


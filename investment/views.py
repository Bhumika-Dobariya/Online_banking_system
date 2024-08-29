

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Investment
from .serializers import InvestmentSerializer
from datetime import datetime


# _____________ Create Investment _____________

@api_view(["POST"])
def create_investment(request):
    serializer = InvestmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# _____________ Get Investment by ID _____________

@api_view(["GET"])
def get_investment_by_id(request):
    investment_id = request.query_params.get('id')
    if not investment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    investment = Investment.objects.filter(id=investment_id, is_active=True).first()
    if investment:
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Investment not found or is inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get All Investments _____________

@api_view(["GET"])
def get_all_investments(request):
    investments = Investment.objects.filter(is_active=True)
    serializer = InvestmentSerializer(investments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# _____________ Update Investment _____________

@api_view(["PUT"])
def update_investment(request):
    investment_id = request.query_params.get('id')
    if not investment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    investment = Investment.objects.filter(id=investment_id, is_active=True).first()
    if investment:
        serializer = InvestmentSerializer(investment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Investment not found or is inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Delete Investment (Mark as Inactive) _____________

@api_view(["DELETE"])
def delete_investment(request):
    investment_id = request.query_params.get('id')
    if not investment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    investment = Investment.objects.filter(id=investment_id, is_active=True).first()
    if investment:
        investment.is_active = False
        investment.save()
        return Response({"detail": "Investment marked as inactive"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Investment not found or is already inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Investments by Type _____________

@api_view(["GET"])
def get_investments_by_type(request):
    investment_type = request.query_params.get('type')
    if not investment_type:
        return Response({"detail": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    investments = Investment.objects.filter(investment_type=investment_type, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found for the specified type or they are inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Investments by Customer ID _____________

@api_view(["GET"])
def get_investments_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(customer_id=customer_id, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found for the specified customer or they are inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Investments by Risk Level _____________

@api_view(["GET"])
def get_investments_by_risk_level(request):
    risk_level = request.query_params.get('risk_level')
    if not risk_level:
        return Response({"detail": "Risk level parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(risk_level=risk_level, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found for the specified risk level or they are inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Investments by Amount Range _____________

@api_view(["GET"])
def get_investments_by_amount_range(request):
    min_amount = request.query_params.get('min_amount')
    max_amount = request.query_params.get('max_amount')

    if not min_amount or not max_amount:
        return Response({"detail": "Both min_amount and max_amount parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(amount__gte=min_amount, amount__lte=max_amount, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found within the specified amount range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)




@api_view(["GET"])
def get_investments_by_maturity_date(request):
    maturity_date = request.query_params.get('maturity_date')
    if not maturity_date:
        return Response({"detail": "Maturity date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        parsed_date = datetime.strptime(maturity_date, "%Y-%m-%d")
    except ValueError:
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
    investments = Investment.objects.filter(maturity_date=parsed_date, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found with the specified maturity date or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_investments_by_interest_rate(request):
    min_rate = request.query_params.get('min_rate')
    max_rate = request.query_params.get('max_rate')

    if not min_rate or not max_rate:
        return Response({"detail": "Both min_rate and max_rate parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(interest_rate__gte=min_rate, interest_rate__lte=max_rate, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found within the specified interest rate range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_investments_by_start_date(request):
    start_date = request.query_params.get('start_date')
    if not start_date:
        return Response({"detail": "Start date parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        parsed_date = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
    investments = Investment.objects.filter(start_date=parsed_date, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found with the specified start date or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_investments_by_roi(request):
    min_roi = request.query_params.get('min_roi')
    max_roi = request.query_params.get('max_roi')

    if not min_roi or not max_roi:
        return Response({"detail": "Both min_roi and max_roi parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(return_on_investment__gte=min_roi, return_on_investment__lte=max_roi, is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found within the specified ROI range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_active_investments(request):
    investments = Investment.objects.filter(is_active=True)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No active investments found"}, status=status.HTTP_404_NOT_FOUND)
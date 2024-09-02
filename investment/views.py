

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Investment
from .serializers import InvestmentSerializer
from datetime import datetime
from decimal import Decimal
from datetime import date

# _____________ Create Investment _____________

@api_view(["POST"])
def create_investment(request):
    serializer = InvestmentSerializer(data=request.data)
    
    if serializer.is_valid():
        investment = serializer.save()
        
        if investment.investment_type == 'fixed_deposit':
            duration_years = (investment.end_date - investment.start_date).days / 365
            if duration_years < 1:
                return Response({"detail": "Fixed Deposit must be at least 1 year long"}, status=status.HTTP_400_BAD_REQUEST)
            investment.total_profit = investment.amount * (Decimal(1) + Decimal(0.10)) ** Decimal(duration_years)
        
        elif investment.investment_type == 'mutual_fund':
            if investment.amount < 5000 or investment.amount > 1000000:
                return Response({"detail": "Mutual Fund amount must be between 5,000 and 1,000,000"}, status=status.HTTP_400_BAD_REQUEST)
            risk_level = "high" if investment.amount > 500000 else "low"
            investment.total_profit = calculate_mutual_fund_profit(investment.amount, risk_level)
        
        elif investment.investment_type == 'stock':
            if investment.start_date < datetime.date.today():
                return Response({"detail": "Start date for stocks cannot be in the past"}, status=status.HTTP_400_BAD_REQUEST)
            volatility_index = get_stock_volatility_index(investment)
            investment.total_profit = investment.amount * (Decimal(1) + Decimal(0.12))
        
        elif investment.investment_type == 'bond':
            if investment.amount < 1000:
                return Response({"detail": "Bond investment amount must be at least 1,000"}, status=status.HTTP_400_BAD_REQUEST)
            if investment.start_date < date.today():
                return Response({"detail": "Start date for bonds cannot be in the past"}, status=status.HTTP_400_BAD_REQUEST)
            investment.total_profit = calculate_bond_profit(investment.amount, investment.investment_rate)
        
        elif investment.investment_type == 'real_estate':
            if investment.amount < 50000:
                return Response({"detail": "Real Estate investment amount must be at least 50,000"}, status=status.HTTP_400_BAD_REQUEST)
            if (investment.end_date - investment.start_date).days < 1825:
                return Response({"detail": "Real Estate investments must be at least 5 years long"}, status=status.HTTP_400_BAD_REQUEST)
            profit_percentage = Decimal('0.06')
            investment.total_profit = investment.amount * profit_percentage
        
        investment.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def calculate_mutual_fund_profit(amount, risk_level):
    return amount * (Decimal('0.08') if risk_level == "low" else Decimal('0.12'))

def get_stock_volatility_index(investment):
    return Decimal('1.05')
def calculate_bond_profit(amount, rate):
    if rate is None:
        rate = Decimal('7.0')  
    else:
        rate = Decimal(rate) 
    
    return amount * (rate / Decimal('100'))


# _____________ Get Investment by ID _____________

@api_view(["GET"])
def get_investment_by_id(request):
    investment_id = request.query_params.get('id')
    if not investment_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    investment = Investment.objects.filter(id=investment_id).first()
    if investment:
        serializer = InvestmentSerializer(investment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Investment not found or is inactive"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get All Investments _____________

@api_view(["GET"])
def get_all_investments(request):
    investments = Investment.objects.filter()
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

    investment = Investment.objects.filter(id=investment_id).first()

    if investment:
        investment.delete()
        return Response({"detail": "Investment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "Investment not found"}, status=status.HTTP_404_NOT_FOUND)

# _____________ Get Investments by Type _____________

@api_view(["GET"])
def get_investments_by_type(request):
    investment_type = request.query_params.get('type')
    if not investment_type:
        return Response({"detail": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    investments = Investment.objects.filter(investment_type=investment_type)
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

    investments = Investment.objects.filter(customer_id=customer_id)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found for the specified customer or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



# _____________ Get Investments by Amount Range _____________

@api_view(["GET"])
def get_investments_by_amount_range(request):
    min_amount = request.query_params.get('min_amount')
    max_amount = request.query_params.get('max_amount')

    if not min_amount or not max_amount:
        return Response({"detail": "Both min_amount and max_amount parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(amount__gte=min_amount, amount__lte=max_amount)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found within the specified amount range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_investments_by_interest_rate(request):
    min_rate = request.query_params.get('min_rate')
    max_rate = request.query_params.get('max_rate')

    if not min_rate or not max_rate:
        return Response({"detail": "Both min_rate and max_rate parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    investments = Investment.objects.filter(investment_rate__gte=min_rate, investment_rate__lte=max_rate)
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found within the specified interest rate range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["GET"])
def get_investments_by_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if not start_date or not end_date:
        return Response({"detail": "Both start date and end date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not (validate_date_format(start_date) and validate_date_format(end_date)):
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
    parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Query investments
    investments = Investment.objects.filter(start_date__gte=parsed_start_date, end_date__lte=parsed_end_date)
    
    if investments.exists():
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No investments found with the specified date range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)


def validate_date_format(date_str):
    """ Validate date format using the format YYYY-MM-DD. """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    



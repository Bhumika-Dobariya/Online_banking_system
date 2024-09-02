from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Insurance
from .serializers import InsuranceSerializer
from decimal import Decimal


@api_view(["POST"])
def create_insurance(request):
    data = request.data
    coverage_amount = data.get('coverage_amount')
    policy_type = data.get('policy_type')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    # Define the fixed premium rate per year
    PREMIUM_PER_YEAR = 10000.00
    
    # Calculate the duration of the insurance in years
    def calculate_premium(start_date, end_date):
        from datetime import datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        duration = (end_date - start_date).days / 365  # Approximate number of years
        return PREMIUM_PER_YEAR * duration
    
    # Calculate premium amount based on provided dates
    if start_date and end_date:
        try:
            premium_amount = calculate_premium(start_date, end_date)
            data['premium_amount'] = premium_amount
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not coverage_amount:
        if policy_type in Insurance.DEFAULT_COVERAGE_AMOUNTS:
            coverage_amount = Insurance.DEFAULT_COVERAGE_AMOUNTS[policy_type]
            data['coverage_amount'] = coverage_amount
    else:
        data['coverage_amount'] = coverage_amount
    
    serializer = InsuranceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_insurance_by_id(request):
    insurance_id = request.query_params.get('id')
    
    if not insurance_id:
        return Response({"error": "Insurance ID is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    insurance = Insurance.objects.filter(id=insurance_id, is_active=True).first()
    
    if insurance:
        serializer = InsuranceSerializer(insurance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Insurance not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_all_insurances(request):

    insurances = Insurance.objects.filter( is_active=True)
    serializer = InsuranceSerializer(insurances, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_insurance(request):
    insurance_id = request.query_params.get('id')
    if not insurance_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    insurance = Insurance.objects.filter(id=insurance_id, is_deleted=False, is_active=True).first()
    if insurance:
        serializer = InsuranceSerializer(insurance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Insurance not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_insurance(request):
    insurance_id = request.query_params.get('id')
    if not insurance_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    insurance = Insurance.objects.filter(id=insurance_id, is_deleted=False, is_active=True).first()
    if insurance:
        insurance.is_deleted = True
        insurance.is_active = False
        insurance.save()
        return Response({"detail": "Insurance marked as deleted and deactivated"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Insurance not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Insurances by Type _____________

@api_view(["GET"])
def get_insurances_by_type(request):
    policy_type = request.query_params.get('type')
    if not policy_type:
        return Response({"detail": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    insurances = Insurance.objects.filter(policy_type=policy_type, is_active=True)
    if insurances.exists():
        serializer = InsuranceSerializer(insurances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No insurances found for the specified type or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Insurances by Provider Name _____________

@api_view(["GET"])
def get_insurances_by_provider(request):
    provider_name = request.query_params.get('provider')
    if not provider_name:
        return Response({"detail": "Provider name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    insurances = Insurance.objects.filter(provider_name__icontains=provider_name, is_active=True)
    if insurances.exists():
        serializer = InsuranceSerializer(insurances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No insurances found with the specified provider name or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Insurances by Coverage Amount _____________

@api_view(["GET"])
def get_insurances_by_coverage_amount(request):
    min_coverage = request.query_params.get('min_coverage')
    max_coverage = request.query_params.get('max_coverage')

    if not min_coverage or not max_coverage:
        return Response({"detail": "Both min_coverage and max_coverage parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    min_coverage = Decimal(min_coverage)
    max_coverage = Decimal(max_coverage)

    insurances = Insurance.objects.filter(
        coverage_amount__gte=min_coverage, 
        coverage_amount__lte=max_coverage, 
        is_active=True  
    )
    
    if insurances.exists():
        serializer = InsuranceSerializer(insurances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({"detail": "No insurances found within the specified coverage amount range"}, status=status.HTTP_404_NOT_FOUND)



# _____________ Get Insurances by Premium Amount _____________


@api_view(["GET"])
def get_insurances_by_premium_amount(request):
    min_premium = request.query_params.get('min_premium')
    max_premium = request.query_params.get('max_premium')

    # Ensure both parameters are provided
    if not min_premium or not max_premium:
        return Response({"detail": "Both min_premium and max_premium parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Filter insurance objects by premium amount range
        insurances = Insurance.objects.filter(
            premium_amount__gte=min_premium,
            premium_amount__lte=max_premium,
            is_active=True
        )

        if insurances.exists():
            serializer = InsuranceSerializer(insurances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": "No insurances found within the specified premium amount range or they are inactive"}, status=status.HTTP_404_NOT_FOUND)

    except (ValueError, TypeError):
        return Response({"detail": "Invalid premium amount format"}, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Active Insurances Only _____________

@api_view(["GET"])
def get_active_insurances(request):
    insurances = Insurance.objects.filter(is_active=True)
    if insurances.exists():
        serializer = InsuranceSerializer(insurances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No active insurances found"}, status=status.HTTP_404_NOT_FOUND)
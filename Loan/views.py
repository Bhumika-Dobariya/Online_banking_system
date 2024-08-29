from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer
from django.utils import timezone


@api_view(["POST"])
def create_loan(request):
    # Extract data from request
    loan_amount = request.data.get('loan_amount')
    interest_rate = request.data.get('interest_rate')
    tenure_months = request.data.get('tenure_months')

    # Validate required fields
    if not loan_amount or not interest_rate or not tenure_months:
        return Response({"detail": "Loan amount, interest rate, and tenure months are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Convert to float for calculation
    loan_amount = float(loan_amount)
    interest_rate = float(interest_rate)
    tenure_months = int(tenure_months)

    # Calculate EMI
    monthly_interest_rate = (interest_rate / 100) / 12
    if monthly_interest_rate > 0:
        emi_amount = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**tenure_months) / ((1 + monthly_interest_rate)**tenure_months - 1)
    else:
        emi_amount = loan_amount / tenure_months 

    emi_amount = round(emi_amount, 2)  

    request.data['emi_amount'] = emi_amount

    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_loan_by_id(request):
    loan_id = request.query_params.get('id')
    if not loan_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    loan = Loan.objects.filter(id=loan_id, is_deleted=False, is_active=True).first()
    if loan:
        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Loan not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_all_loans(request):
    loans = Loan.objects.filter(is_deleted=False, is_active=True)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_loan(request):
    loan_id = request.query_params.get('id')
    if not loan_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    loan = Loan.objects.filter(id=loan_id, is_deleted=False, is_active=True).first()
    if loan:
        serializer = LoanSerializer(loan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Loan not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_loan(request):
    loan_id = request.query_params.get('id')
    if not loan_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    loan = Loan.objects.filter(id=loan_id, is_deleted=False, is_active=True).first()
    if loan:
        loan.is_deleted = True
        loan.is_active = False
        loan.save()
        return Response({"detail": "Loan marked as deleted and deactivated"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Loan not found or is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Loans by Type _____________

@api_view(["GET"])
def get_loans_by_type(request):
    loan_type = request.query_params.get('loan_type')
    if not loan_type:
        return Response({"detail": "Loan type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    loans = Loan.objects.filter(loan_type=loan_type, is_deleted=False, is_active=True)
    if loans.exists():
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No loans found for the specified type or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


# _____________ Get Loans by Customer ID _____________

@api_view(["GET"])
def get_loans_by_customer(request):
    customer_id = request.query_params.get('customer_id')
    if not customer_id:
        return Response({"detail": "Customer ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    loans = Loan.objects.filter(customer_id=customer_id, is_deleted=False, is_active=True)
    if loans.exists():
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No loans found for the specified customer or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def get_loans_by_status(request):
    status_param = request.query_params.get('status')
    if not status_param:
        return Response({"detail": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    loans = Loan.objects.filter(status=status_param, is_deleted=False, is_active=True)
    if loans.exists():
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No loans found with the specified status or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_loans_by_date_range(request):
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if not start_date or not end_date:
        return Response({"detail": "Start date and end date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        start_date = timezone.datetime.fromisoformat(start_date)
        end_date = timezone.datetime.fromisoformat(end_date)
    except ValueError:
        return Response({"detail": "Invalid date format. Use ISO 8601 format."}, status=status.HTTP_400_BAD_REQUEST)
    
    loans = Loan.objects.filter(applied_date__range=[start_date, end_date], is_deleted=False, is_active=True)
    if loans.exists():
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No loans found in the specified date range or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_loans_by_customer_and_status(request):
    customer_id = request.query_params.get('customer_id')
    status_param = request.query_params.get('status')
    
    if not customer_id or not status_param:
        return Response({"detail": "Customer ID and status parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    loans = Loan.objects.filter(customer_id=customer_id, status=status_param, is_deleted=False, is_active=True)
    if loans.exists():
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No loans found for the specified customer and status or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def get_overdue_loans(request):
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(due_date__lt=today, is_deleted=False, is_active=True)
    
    if overdue_loans.exists():
        serializer = LoanSerializer(overdue_loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "No overdue loans found or they are inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from .serializers import LoanSerializer
from django.utils import timezone
from datetime import datetime


@api_view(["POST"])
def create_loan(request):
    loan_amount = request.data.get('loan_amount')
    tenure_months = request.data.get('tenure_months')
    loan_type = request.data.get('loan_type')

    if not loan_amount or not tenure_months or not loan_type:
        return Response({"detail": "Loan amount, tenure months, and loan type are required"}, status=status.HTTP_400_BAD_REQUEST)

    loan_amount = float(loan_amount)
    tenure_months = int(tenure_months)

    # Fetch interest rate and processing fee based on loan type
    interest_rates = Loan.INTEREST_RATES
    processing_fees = Loan.PROCESSING_FEES

    interest_rate = interest_rates.get(loan_type, 0.0)
    processing_fee_percentage = processing_fees.get(loan_type, 0.0)
    processing_fee = round(loan_amount * processing_fee_percentage, 2)

    # Calculate EMI
    monthly_interest_rate = (interest_rate / 100) / 12
    if monthly_interest_rate > 0:
        emi_amount = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**tenure_months) / ((1 + monthly_interest_rate)**tenure_months - 1)
    else:
        emi_amount = loan_amount / tenure_months  
    emi_amount = round(emi_amount, 2)  
    request.data['emi_amount'] = emi_amount
    request.data['interest_rate'] = interest_rate
    request.data['processing_fee'] = processing_fee

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
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')
    
    if not start_date_str or not end_date_str:
        return Response({"detail": "Start date and end date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        end_date = datetime.combine(end_date, datetime.max.time())
    except ValueError:
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)
    
    loans = Loan.objects.filter(
        applied_date__range=[start_date, end_date],is_deleted=False,is_active=True)
    
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


@api_view(["POST"])
def approve_loan(request):
    loan_id = request.query_params.get('loan_id')
    
    if not loan_id:
        return Response({"detail": "Loan ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    loan = Loan.objects.filter(id=loan_id, is_deleted=False, is_active=True).first()

    if not loan:
        return Response({"detail": "Loan not found or it is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)

    loan.status = 'approved'
    loan.approved_date = timezone.now()
    loan.save()

    serializer = LoanSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def update_loan_status(request):
    loan_id = request.query_params.get('loan_id')
    new_status = request.query_params.get('status')

    if not loan_id:
        return Response({"detail": "Loan ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not new_status:
        return Response({"detail": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    status_choices = dict(Loan.LOAN_STATUS_CHOICES)  
    if new_status not in status_choices:
        return Response({"detail": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
    
    loan = Loan.objects.filter(id=loan_id, is_deleted=False, is_active=True).first()
    
    if not loan:
        return Response({"detail": "Loan not found or it is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)
    
    loan.status = new_status
    loan.save()

    serializer = LoanSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def complete_loan(request):
    loan_id = request.query_params.get('loan_id')
    
    if not loan_id:
        return Response({"detail": "Loan ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    loan = Loan.objects.filter(id=loan_id, is_deleted=False, is_active=True).first()

    if not loan:
        return Response({"detail": "Loan not found or it is inactive/deleted"}, status=status.HTTP_404_NOT_FOUND)

    if loan.status != 'disbursed':
        return Response({"detail": "Loan must be in 'disbursed' status to be marked as complete"}, status=status.HTTP_400_BAD_REQUEST)

    loan.status = 'closed'
    loan.save()

    serializer = LoanSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)

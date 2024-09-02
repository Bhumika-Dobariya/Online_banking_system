from django.urls import path
from .views import (
    create_loan,
    get_loan_by_id,
    get_all_loans,
    update_loan,
    delete_loan,
    get_loans_by_type,
    get_loans_by_customer,
    get_loans_by_status,
    get_loans_by_date_range,
    get_loans_by_customer_and_status,
    approve_loan,
    update_loan_status,
    complete_loan
    
)

urlpatterns = [
    path('create_loan/', create_loan, name='create_loan'),
    path('get_loan_by_id/', get_loan_by_id, name='get_loan_by_id'),
    path('get_all_loans/', get_all_loans, name='get_all_loans'),
    path('update_loan/', update_loan, name='update_loan'),
    path('delete_loan/', delete_loan, name='delete_loan'),
    path('get_loans_by_type/', get_loans_by_type, name='get_loans_by_type'),
    path('get_loans_by_customer/', get_loans_by_customer, name='get_loans_by_customer'),
    path('get_loans_by_status/', get_loans_by_status, name='get_loans_by_status'),
    path('get_loans_by_date_range/', get_loans_by_date_range, name='get_loans_by_date_range'),
    path('get_loans_by_customer_and_status/', get_loans_by_customer_and_status, name='get_loans_by_customer_and_status'),
    path('approve_loan/', approve_loan, name='approve_loan'),
    path('update_loan_status/', update_loan_status, name='update_loan_status'),
    path('complete_loan/', complete_loan, name='complete_loan'),


]


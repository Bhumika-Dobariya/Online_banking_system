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
    get_overdue_loans
)

urlpatterns = [
    path('create/', create_loan, name='create_loan'),
    path('get/', get_loan_by_id, name='get_loan_by_id'),
    path('all/', get_all_loans, name='get_all_loans'),
    path('update/', update_loan, name='update_loan'),
    path('delete/', delete_loan, name='delete_loan'),
    path('by_type/', get_loans_by_type, name='get_loans_by_type'),
    path('by_customer/', get_loans_by_customer, name='get_loans_by_customer'),
    path('by_status/', get_loans_by_status, name='get_loans_by_status'),
    path('by_date_range/', get_loans_by_date_range, name='get_loans_by_date_range'),
    path('by_customer_and_status/', get_loans_by_customer_and_status, name='get_loans_by_customer_and_status'),
    path('overdue/', get_overdue_loans, name='get_overdue_loans'),
]


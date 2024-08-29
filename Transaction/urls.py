from django.urls import path
from . import views 

urlpatterns = [
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('transactions/', views.get_transaction_by_id, name='get_transaction_by_id'),
    path('transactions/', views.get_all_transactions, name='get_all_transactions'),
    path('transactions/update/', views.update_transaction, name='update_transaction'),
    path('transactions/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/type/', views.get_transactions_by_type, name='get_transactions_by_type'),
    path('transactions/date_range/', views.get_transactions_by_date_range, name='get_transactions_by_date_range'),
    path('transactions/status/', views.get_transactions_by_status, name='get_transactions_by_status'),
    path('transactions/account/', views.get_transactions_by_account, name='get_transactions_by_account'),
]


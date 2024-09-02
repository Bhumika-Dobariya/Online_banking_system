from django.urls import path
from . import views 

urlpatterns = [
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('get_transaction_by_id/', views.get_transaction_by_id, name='get_transaction_by_id'),
    path('get_all_transactions/', views.get_all_transactions, name='get_all_transactions'),
    path('update_transaction/', views.update_transaction, name='update_transaction'),
    path('delete_transaction/', views.delete_transaction, name='delete_transaction'),
    path('get_transactions_by_type/', views.get_transactions_by_type, name='get_transactions_by_type'),
    path('get_transactions_by_date_range/', views.get_transactions_by_date_range, name='get_transactions_by_date_range'),
    path('get_transactions_by_status/', views.get_transactions_by_status, name='get_transactions_by_status'),
    path('get_transactions_by_account/', views.get_transactions_by_account, name='get_transactions_by_account'),
    path('get_transactions_by_customer/', views.get_transactions_by_customer, name='get_transactions_by_customer'),
    path('get_transactions_by_amount_range/', views.get_transactions_by_amount_range, name='get_transactions_by_amount_range'),


]


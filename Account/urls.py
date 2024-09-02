from django.urls import path
from . import views

urlpatterns = [
    path('create_account/', views.create_account, name='create_account'),
    path('get_account_by_id/', views.get_account_by_id, name='get_account_by_id'),
    path('get_all_accounts/', views.get_all_accounts, name='get_all_accounts'),
    path('update_account/', views.update_account, name='update_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('get_accounts_by_type/', views.get_accounts_by_type, name='get_accounts_by_type'),
    path('get_accounts_by_customer/', views.get_accounts_by_customer, name='get_accounts_by_user'),
    path('toggle_account_status/', views.toggle_account_status, name='toggle_account_status'),
    path('filter_accounts_by_balance/', views.filter_accounts_by_balance, name='filter_accounts_by_balance'),
    path('transfer_funds/', views.transfer_funds, name='transfer_funds'),
    path('get_personal_accounts/', views.get_personal_accounts, name='get_personal_accounts'),


]


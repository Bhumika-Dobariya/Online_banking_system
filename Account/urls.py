from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_account, name='create_account'),
    path('get/', views.get_account_by_id, name='get_account_by_id'),
    path('all/', views.get_all_accounts, name='get_all_accounts'),
    path('update/', views.update_account, name='update_account'),
    path('delete/', views.delete_account, name='delete_account'),
    path('by-type/', views.get_accounts_by_type, name='get_accounts_by_type'),
    path('by-user/', views.get_accounts_by_user, name='get_accounts_by_user'),
    path('toggle-status/', views.toggle_account_status, name='toggle_account_status'),
    path('filter-by-balance/', views.filter_accounts_by_balance, name='filter_accounts_by_balance'),
    path('transfer-funds/', views.transfer_funds, name='transfer_funds'),
    path('by-balance-gt/', views.get_accounts_by_balance_gt, name='get_accounts_by_balance_gt'),
    path('by-balance-gt/', views.get_accounts_by_balance_gt, name='get_accounts_by_balance_gt'),


]




from django.urls import path
from . import views

urlpatterns = [
    path('create_investment/', views.create_investment, name='create_investment'),
    path('get_investment_by_id/', views.get_investment_by_id, name='get_investment_by_id'),
    path('get_all_investments/', views.get_all_investments, name='get_all_investments'),
    path('update_investment/', views.update_investment, name='update_investment'),
    path('delete_investment/', views.delete_investment, name='delete_investment'),
    path('get_investments_by_type/', views.get_investments_by_type, name='get_investments_by_type'),
    path('get_investments_by_customer/', views.get_investments_by_customer, name='get_investments_by_customer'),
    path('get_investments_by_amount_range/', views.get_investments_by_amount_range, name='get_investments_by_amount_range'),
    path('get_investments_by_interest_rate/', views.get_investments_by_interest_rate, name='get_investments_by_interest_rate'),
    path('get_investments_by_date_range/', views.get_investments_by_date_range, name='get_investments_by_date_range'),
]
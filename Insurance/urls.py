from django.urls import path
from .views import (
    create_insurance,
    get_insurance_by_id,
    get_all_insurances,
    update_insurance,
    delete_insurance,
    get_insurances_by_type,
    get_insurances_by_provider,
    get_insurances_by_coverage_amount,
    get_insurances_by_premium_amount,
    get_active_insurances
)

urlpatterns = [
    path('create_insurance/', create_insurance, name='create_insurance'),
    path('get_insurance_by_id/', get_insurance_by_id, name='get_insurance_by_id'),
    path('get_all_insurances/', get_all_insurances, name='get_all_insurances'),
    path('update_insurance/', update_insurance, name='update_insurance'),
    path('delete_insurance/', delete_insurance, name='delete_insurance'),
    path('get_insurances_by_type/', get_insurances_by_type, name='get_insurances_by_type'),
    path('get_insurances_by_provider/', get_insurances_by_provider, name='get_insurances_by_provider'),
    path('get_insurances_by_coverage_amount/', get_insurances_by_coverage_amount, name='get_insurances_by_coverage_amount'),
    path('get_insurances_by_premium_amount/', get_insurances_by_premium_amount, name='get_insurances_by_premium_amount'),
    path('get_active_insurances/', get_active_insurances, name='get_active_insurances'),
]

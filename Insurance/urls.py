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
    path('create/', create_insurance, name='create_insurance'),
    path('retrieve/', get_insurance_by_id, name='get_insurance_by_id'),
    path('list/', get_all_insurances, name='get_all_insurances'),
    path('update/', update_insurance, name='update_insurance'),
    path('delete/', delete_insurance, name='delete_insurance'),
    path('by_type/', get_insurances_by_type, name='get_insurances_by_type'),
    path('by_provider/', get_insurances_by_provider, name='get_insurances_by_provider'),
    path('by_coverage/', get_insurances_by_coverage_amount, name='get_insurances_by_coverage_amount'),
    path('by_premium/', get_insurances_by_premium_amount, name='get_insurances_by_premium_amount'),
    path('active/', get_active_insurances, name='get_active_insurances'),
]

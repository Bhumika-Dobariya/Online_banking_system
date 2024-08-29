from django.urls import path
from . import views

urlpatterns = [
    path('create_customer/', views.create_customer, name='create_customer'),
    path('get_customer_by_id/', views.get_customer_by_id, name='get_customer_by_id'),
    path('get_all_customers/', views.get_all_customers, name='get_all_customers'),
    path('update_customer/', views.update_customer, name='update_customer'),
    path('delete_customer/', views.delete_customer, name='delete_customer'),
    path('get_customers_by_gender/', views.get_customers_by_gender, name='get_customers_by_gender'),
    path('get_customers_by_name/', views.get_customers_by_name, name='get_customers_by_name'),
]

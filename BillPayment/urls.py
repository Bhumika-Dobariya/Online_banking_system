from django.urls import path
from . import views

urlpatterns = [
    path('create_bill_payment/', views.create_bill_payment, name='create_bill_payment'),
    path('get_bill_payment_by_id/', views.get_bill_payment_by_id, name='get_bill_payment_by_id'),
    path('get_all_bill_payments/', views.get_all_bill_payments, name='get_all_bill_payments'),
    path('update_bill_payment/', views.update_bill_payment, name='update_bill_payment'),
    path('delete_bill_payment/', views.delete_bill_payment, name='delete_bill_payment'),
    path('get_bill_payments_by_customer/', views.get_bill_payments_by_customer, name='get_bill_payments_by_customer'),
    path('get_bill_payments_by_payment_type/', views.get_bill_payments_by_payment_type, name='get_bill_payments_by_payment_type'),
    path('get_bill_payments_by_due_date_range/', views.get_bill_payments_by_due_date_range, name='get_bill_payments_by_due_date_range'),
    path('get_bill_payments_by_payment_method/', views.get_bill_payments_by_payment_method, name='get_bill_payments_by_payment_method'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('create_support_request/', views.create_support_request, name='create_support_request'),
    path('get_support_request_by_id/', views.get_support_request_by_id, name='get_support_request_by_id'),
    path('get_all_support_requests/', views.get_all_support_requests, name='get_all_support_requests'),
    path('update_support_request/', views.update_support_request, name='update_support_request'),
    path('delete_support_request/', views.delete_support_request, name='delete_support_request'),
    path('get_support_requests_by_status/', views.get_support_requests_by_status, name='get_support_requests_by_status'),
    path('get_support_requests_by_customer/', views.get_support_requests_by_customer, name='get_support_requests_by_customer'),
    path('close_support_request/', views.close_support_request, name='close_support_request'),
]

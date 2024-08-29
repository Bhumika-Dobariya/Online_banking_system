from django.urls import path
from . import views

urlpatterns = [
    path('support/create/', views.create_support_request, name='create_support_request'),
    path('support/', views.get_support_request_by_id, name='get_support_request_by_id'),
    path('support/', views.get_all_support_requests, name='get_all_support_requests'),
    path('support/update/', views.update_support_request, name='update_support_request'),
    path('support/delete/', views.delete_support_request, name='delete_support_request'),
    path('support/status/', views.get_support_requests_by_status, name='get_support_requests_by_status'),
    path('support/customer/', views.get_support_requests_by_customer, name='get_support_requests_by_customer'),
    path('support/close/', views.close_support_request, name='close_support_request'),
    path('support/search/', views.search_support_requests, name='search_support_requests'),
]

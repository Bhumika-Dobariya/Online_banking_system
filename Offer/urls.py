from django.urls import path
from . import views

urlpatterns = [
    path('create_offer/', views.create_offer, name='create_offer'),
    path('get_offer_by_id/', views.get_offer_by_id, name='get_offer_by_id'),
    path('get_all_offers/', views.get_all_offers, name='get_all_offers'),
    path('update_offer/', views.update_offer, name='update_offer'),
    path('delete_offer/', views.delete_offer, name='delete_offer'),
    path('get_active_offers/', views.get_active_offers, name='get_active_offers'),
    path('activate_offer/', views.activate_offer, name='activate_offer'),
    path('deactivate_offer/', views.deactivate_offer, name='deactivate_offer'),
    path('get_offers_by_type/', views.get_offers_by_type, name='get_offers_by_type'),
    path('get_offers_by_status/', views.get_offers_by_status, name='get_offers_by_status'),
    path('extend_offer_duration/', views.extend_offer_duration, name='extend_offer_duration'),
]

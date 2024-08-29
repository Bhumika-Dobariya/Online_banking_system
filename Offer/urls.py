from django.urls import path
from .views import (
    create_offer,
    get_offer_by_id,
    get_all_offers,
    update_offer,
    delete_offer,
    get_active_offers,
)

urlpatterns = [
    path('offer/create/', create_offer, name='create_offer'),
    path('offer/', get_offer_by_id, name='get_offer_by_id'),
    path('offers/', get_all_offers, name='get_all_offers'),
    path('offer/update/', update_offer, name='update_offer'),
    path('offer/delete/', delete_offer, name='delete_offer'),
    path('offers/active/', get_active_offers, name='get_active_offers'),
]

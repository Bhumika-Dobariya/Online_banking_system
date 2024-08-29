from django.urls import path
from . import views

urlpatterns = [
    path('create_card/', views.create_card, name='create_card'),
    path('get_card_by_id/', views.get_card_by_id, name='get_card_by_id'),
    path('get_all_cards/', views.get_all_cards, name='get_all_cards'),
    path('update_card/', views.update_card, name='update_card'),
    path('delete_card/', views.delete_card, name='delete_card'),
    path('get_cards_by_type/', views.get_cards_by_type, name='get_cards_by_type'),
    path('get_cards_by_customer/', views.get_cards_by_customer, name='get_cards_by_customer'),
    path('filter_cards_by_balance/', views.filter_cards_by_balance, name='filter_cards_by_balance'),
    path('transfer_funds_between_cards/', views.transfer_funds_between_cards, name='transfer_funds_between_cards'),
    path('deactivate_card/', views.deactivate_card, name='deactivate_card'),
    path('reactivate_card/', views.reactivate_card, name='reactivate_card'),
    path('get_expiring_cards/', views.get_expiring_cards, name='get_expiring_cards'),
    path('update_card_pin/', views.update_card_pin, name='update_card_pin'),
    path('get_cards_by_bank/', views.get_cards_by_bank, name='get_cards_by_bank'),
    path('get_card_with_transactions/', views.get_card_with_transactions, name='get_card_with_transactions'),
]

from rest_framework import serializers
from .models import Offer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'title', 'offer_type', 'discount_percentage', 'cashback_amount', 'valid_from', 'valid_until', 'applicable_to', 'entity_id', 'is_active']
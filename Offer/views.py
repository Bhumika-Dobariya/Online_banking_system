from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Offer
from .serializers import OfferSerializer

# Create Offer

@api_view(["POST"])
def create_offer(request):
    serializer = OfferSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Get Offer by ID
@api_view(["GET"])
def get_offer_by_id(request):
    offer_id = request.query_params.get('id')
    if not offer_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.filter(id=offer_id, is_active=True).first()
    if offer:
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"detail": "Offer not found or inactive"}, status=status.HTTP_404_NOT_FOUND)

# Get All Offers
@api_view(["GET"])
def get_all_offers(request):
    offers = Offer.objects.filter(is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Update Offer
@api_view(["PUT"])
def update_offer(request):
    offer_id = request.query_params.get('id')
    if not offer_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.filter(id=offer_id, is_active=True).first()
    if offer:
        serializer = OfferSerializer(offer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Offer not found or inactive"}, status=status.HTTP_404_NOT_FOUND)

# Delete Offer
@api_view(["DELETE"])
def delete_offer(request):
    offer_id = request.query_params.get('id')
    if not offer_id:
        return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.filter(id=offer_id, is_active=True).first()
    if offer:
        offer.delete()
        return Response({"detail": "Offer deleted"}, status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Offer not found or inactive"}, status=status.HTTP_404_NOT_FOUND)

# Get Active Offers
@api_view(["GET"])
def get_active_offers(request):
    now = timezone.now()
    offers = Offer.objects.filter(is_active=True, start_date__lte=now, end_date__gte=now)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Activate Offer
@api_view(["POST"])
def activate_offer(request):
    offer_id = request.query_params.get('offer_id')
    if not offer_id:
        return Response({"detail": "Offer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.filter(id=offer_id).first()
    if offer:
        offer.is_active = True
        offer.save()
        return Response({"detail": "Offer activated"}, status=status.HTTP_200_OK)
    return Response({"detail": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)

# Deactivate Offer
@api_view(["POST"])
def deactivate_offer(request):
    offer_id = request.query_params.get('offer_id')
    if not offer_id:
        return Response({"detail": "Offer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.filter(id=offer_id).first()
    if offer:
        offer.is_active = False
        offer.save()
        return Response({"detail": "Offer deactivated"}, status=status.HTTP_200_OK)
    return Response({"detail": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)

# Get Offers by Type
@api_view(["GET"])
def get_offers_by_type(request):
    offer_type = request.query_params.get('offer_type')
    if not offer_type:
        return Response({"detail": "Offer type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    offers = Offer.objects.filter(offer_type=offer_type, is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Get Offers by Status
@api_view(["GET"])
def get_offers_by_status(request):
    status_param = request.query_params.get('status')
    if not status_param:
        return Response({"detail": "Status parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    offers = Offer.objects.filter(status=status_param, is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Extend Offer Duration
@api_view(["PUT"])
def extend_offer_duration(request):
    offer_id = request.query_params.get('id')
    new_end_date = request.data.get('new_end_date')
    if not offer_id or not new_end_date:
        return Response({"detail": "ID and new end date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

    offer = Offer.objects.filter(id=offer_id).first()
    if offer:
        offer.end_date = timezone.make_aware(new_end_date)
        offer.save()
        return Response({"detail": "Offer duration extended"}, status=status.HTTP_200_OK)
    return Response({"detail": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)

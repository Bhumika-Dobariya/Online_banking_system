from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Offer
from .serializers import OfferSerializer

# _____________ Create Offer _____________

@api_view(["POST"])
def create_offer(request):
    serializer = OfferSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____________ Get Offer by ID _____________

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

# _____________ Get All Offers _____________

@api_view(["GET"])
def get_all_offers(request):
    offers = Offer.objects.filter(is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# _____________ Update Offer _____________

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

# _____________ Delete Offer _____________

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

# _____________ Get Active Offers _____________

@api_view(["GET"])
def get_active_offers(request):
    now = timezone.now()
    offers = Offer.objects.filter(is_active=True, valid_from__lte=now, valid_until__gte=now)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

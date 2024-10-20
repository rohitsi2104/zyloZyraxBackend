
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import Zylo_Banner, Zylo_Offer
from .serializers import BannerSerializer, OfferSerializer



@api_view(['GET'])
@permission_classes([AllowAny])
def get_banners(request):
    banners = Zylo_Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_offers(request):
    offers = Zylo_Offer.objects.filter(is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)

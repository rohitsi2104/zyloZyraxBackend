
from rest_framework import serializers
from .models import Zylo_Banner, Zylo_Offer
from django.contrib.auth.models import User

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zylo_Banner
        fields = ['id', 'title', 'image', 'description']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zylo_Offer
        fields = ['id', 'title', 'amount', 'discount', 'duration', 'description', 'is_active']

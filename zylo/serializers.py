
from rest_framework import serializers
from .models import Zylo_Banner, Zylo_Offer, Zylo_Class
from django.contrib.auth.models import User

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zylo_Banner
        fields = ['id', 'title', 'image', 'description']

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zylo_Offer
        fields = ['id', 'title', 'amount', 'discount', 'duration', 'description', 'is_active']





class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zylo_Class
        fields = '__all__'

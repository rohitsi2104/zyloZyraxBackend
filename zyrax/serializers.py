from rest_framework import serializers
from .models import Banner, Offer, Zyrax_Class, UserProfile, CommunityPost, PostImage, Comment, Tutors, Service_Post, \
    Attendance, UserAdditionalInfo
from django.contrib.auth.models import User


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'description']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id', 'title', 'amount', 'discount', 'duration', 'description', 'is_active']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zyrax_Class
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'date_of_birth']


class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutors
        fields = ['first_name', 'last_name', 'image', 'video_link', 'description']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()  # Nested UserProfile

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}}  # Password should be write-only

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        UserProfile.objects.create(user=user, **profile_data)  # Create UserProfile
        return user


class CommunityPostSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True)  # List of image URLs for the post

    class Meta:
        model = CommunityPost
        fields = ['id', 'user', 'content', 'images', 'created_at']


# Post Image Serializer
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'post', 'image']


# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']


class ServicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service_Post
        fields = ['id', 'title', 'image', 'description']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'date', 'created_at']
        read_only_fields = ['user', 'created_at']


class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdditionalInfo
        fields = ['profile_picture', 'height', 'weight', 'gender', 'address']


class FullUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerialize()
    additional_info = UserAdditionalInfoSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'additional_info']

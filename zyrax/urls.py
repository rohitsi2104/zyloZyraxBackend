from django.urls import path
from .views import (
    get_banners,
    get_offers,
    register,
    verify_otp,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    get_posts,
    create_post,
    create_comment,
    get_comments,
    admin_register,
    get_classes,
    get_tutor_profile
)

urlpatterns = [
    path('banners/', get_banners, name='get_banners'),
    path('offers/', get_offers, name='get_offers'),
    path('register/', register, name='register_user'),
    path('verify-otp/', verify_otp, name='verify_otp'),  # New path for OTP verification
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', get_posts, name='get_posts'),
    path('posts/create/', create_post, name='create_post'),
    path('posts/<int:post_id>/comments/', get_comments, name='get_comments'),
    path('posts/<int:post_id>/comments/create/', create_comment, name='create_comment'),
    path('admin/register/', admin_register, name='admin-register'),
    path('classes/', get_classes, name='get_classes'),
    path('get_tutor_profile/', get_tutor_profile, name='get_tutor_profile')
]

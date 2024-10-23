
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Banner, Offer, CommunityPost, PostImage, Comment, UserProfile , Zyrax_Class
from .serializers import BannerSerializer, OfferSerializer, CommunityPostSerializer, PostImageSerializer, CommentSerializer ,ClassSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.core.cache import cache
import random
import string
import http.client
import json
from django.shortcuts import render
from django.conf import settings

# Define the Msg91 authentication and template IDs
YOUR_TEMPLATE_ID = "6713a05bd6fc05281162ae92"
AUTH_KEY = "432827AWgMjqCXpNu6713a234P1"

# Function to send OTP via Msg91
def send_otp(phone_number, otp):
    conn = http.client.HTTPSConnection("control.msg91.com")
    payload = json.dumps({
        "otp": otp,
        "mobile": phone_number,
        "template_id": YOUR_TEMPLATE_ID,
        "authkey": AUTH_KEY,
        "otp_expiry": 15
    })
    url = f"/api/v5/otp?template_id=YOUR_TEMPLATE_ID&mobile={phone_number}&authkey={AUTH_KEY}&otp_expiry=15"
    conn.request("POST", url, payload, headers={"Content-Type": "application/json"})
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Function to generate a random password
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Homepage View
def homepage_view(request):
    return render(request, 'readme.html')

# Banner View
@api_view(['GET'])
@permission_classes([AllowAny])
def get_banners(request):
    banners = Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

# Zylo_Offer View
@api_view(['GET'])
@permission_classes([AllowAny])
def get_offers(request):
    offers = Offer.objects.filter(is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_classes(request):
    classes = Zyrax_Class.objects.all()
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)

# User Registration API (via OTP)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone_number = request.data.get('phone_number')
    date_of_birth = request.data.get('date_of_birth')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    if phone_number and password and confirm_password:
        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=phone_number).exists():
            return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

        otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        cache.set(f'otp_{phone_number}', otp, timeout=300)
        send_otp(phone_number, otp)

        cache.set(f'registration_data_{phone_number}', {
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth,
            'password': password
        }, timeout=300)

        return Response({"message": "OTP sent to your phone"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

# Verify OTP
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    phone_number = request.data.get('phone_number')
    otp_entered = request.data.get('otp')
    stored_otp = cache.get(f'otp_{phone_number}')

    if stored_otp and stored_otp == otp_entered:
        registration_data = cache.get(f'registration_data_{phone_number}')
        if registration_data:
            user = User.objects.create_user(
                username=phone_number,
                password=registration_data['password'],
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name']
            )
            UserProfile.objects.create(
                user=user,
                first_name=registration_data['first_name'],
                last_name=registration_data['last_name'],
                phone_number=phone_number,
                date_of_birth=registration_data['date_of_birth']
            )
            cache.delete(f'registration_data_{phone_number}')
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "No registration data found"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

# Admin Register User API (no OTP)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    phone_number = request.data.get('phone_number')
    date_of_birth = request.data.get('date_of_birth')
    password = request.data.get('password')

    if not phone_number:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=phone_number).exists():
        return Response({"error": "Phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a random password if none is provided
    if not password:
        password = generate_random_password()

    # Create the user
    user = User.objects.create_user(
        username=phone_number,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    UserProfile.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        date_of_birth=date_of_birth
    )

    # Here you can send the password to the admin or the user
    return Response({"message": "User created successfully", "password": password}, status=status.HTTP_201_CREATED)

# Login View
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')

    user = User.objects.filter(username=phone_number).first()
    if user and user.check_password(password):
        token_obtain_view = TokenObtainPairView.as_view()
        return token_obtain_view(request)
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Community Post API Endpoints
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    content = request.data.get('content')
    images = request.FILES.getlist('images')

    post = CommunityPost.objects.create(user=request.user, content=content)

    for image in images:
        PostImage.objects.create(post=post, image=image)

    serializer = CommunityPostSerializer(post)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_posts(request):
    posts = CommunityPost.objects.all().prefetch_related('images')
    serializer = CommunityPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
    content = request.data.get('content')
    post = CommunityPost.objects.get(id=post_id)
    comment = Comment.objects.create(post=post, user=request.user, content=content)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments(request, post_id):
    post = CommunityPost.objects.get(id=post_id)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# Token Views
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView

from .models import Zylo_Banner, Zylo_Offer, CommunityPost, PostImage, Comments, UserProfile, Zylo_Class, Tutors, \
    Service_Post, Attendance, UserAdditionalInfo, Zylo_Testimonial, Zylo_CallbackRequest
from .serializers import BannerSerializer, OfferSerializer, CommunityPostSerializer, PostImageSerializer, \
    CommentSerializer, ClassSerializer, TutorProfileSerializer, ServicePostSerializer, AttendanceSerializer, \
    FullUserProfileSerializer, UserAdditionalInfoSerializer, Zylo_TestionialSerializer, Zylo_CallbackRequestSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.core.cache import cache
import random
import string
import http.client
import json
from django.shortcuts import render
from django.utils import timezone
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


@api_view(['GET'])
@permission_classes([AllowAny])
def get_banners(request):
    banners = Zylo_Banner.objects.all()
    serializer = BannerSerializer(banners, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def callback_request(request):
    # Handle GET request
    if request.method == 'GET':
        # Return all callback requests (or modify to filter as needed)
        callback_requests = Zylo_CallbackRequest.objects.all()
        serializer = Zylo_CallbackRequestSerializer(callback_requests, many=True)
        return Response(serializer.data)

    # Handle POST request
    elif request.method == 'POST':
        # Create a new callback request
        serializer = Zylo_CallbackRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Testimonial
@api_view(['GET'])
@permission_classes([AllowAny])
def get_testimonials(request):
    testimonial = Zylo_Testimonial.objects.all()
    serializer = Zylo_TestionialSerializer(testimonial, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_offers(request):
    offers = Zylo_Offer.objects.filter(is_active=True)
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_classes(request):
    classes = Zylo_Class.objects.all()
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
        print(otp)
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
    comment = Comments.objects.create(post=post, user=request.user, content=content)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_comments(request, post_id):
    post = CommunityPost.objects.get(id=post_id)
    comments = post.comments.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_tutor_profile(request):
    tutors = Tutors.objects.all()
    serializer = TutorProfileSerializer(tutors, many=True)
    return Response(serializer.data)


# Service_Post
@api_view(['Get'])
@permission_classes([AllowAny])
def service_post(request):
    service_post = Service_Post.objects.all()
    serializer = ServicePostSerializer(service_post, many=True)
    return Response(serializer.data)


# Token Views
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


class AttendanceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def mark_attendance(self, request):
        user = request.user
        today = timezone.now().date()

        if Attendance.objects.filter(user=user, date=today).exists():
            return Response({"detail": "Attendance already marked for today."}, status=status.HTTP_400_BAD_REQUEST)

        attendance = Attendance.objects.create(user=user, date=today)
        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='monthly_attendance/(?P<user_id>[^/.]+)')
    def monthly_attendance(self, request, user_id=None):
        """
        Retrieve monthly attendance for a specific user to show on a calendar.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        month_str = request.query_params.get('month')
        year_str = request.query_params.get('year')

        if not month_str or not year_str:
            return Response({"detail": "Month and year parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month_str)
            year = int(year_str)
            start_date = datetime(year, month, 1).date()
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        except ValueError:
            return Response({"detail": "Invalid month or year format."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch attendance records for the specified month
        attendance_records = Attendance.objects.filter(user=user, date__range=[start_date, end_date])

        # Create a dictionary for the entire month with default "Absent" status
        days_in_month = (end_date - start_date).days + 1
        attendance_summary = {start_date + timedelta(days=i): "Absent" for i in range(days_in_month)}

        # Mark the dates the user was present
        for record in attendance_records:
            attendance_summary[record.date] = "Present"

        # Convert attendance_summary to a list of dictionaries for JSON response
        attendance_data = [
            {"date": day.strftime("%Y-%m-%d"), "status": status}
            for day, status in attendance_summary.items()
        ]

        return Response(attendance_data, status=status.HTTP_200_OK)


class UserProfileDetailsView(APIView):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = FullUserProfileSerializer(user_profile)
        return Response(serializer.data)


@api_view(['POST'])
def create_or_update_user_additional_info(request, user_id):
    try:
        # Get the User instance using the provided user_id
        user = User.objects.get(id=user_id)

        # Fetch the related UserProfile using the related_name 'zyrax_user_profile'
        user_profile = user.zyrax_user_profile  # Using the related_name

    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except UserProfile.DoesNotExist:
        return Response({"detail": "UserProfile not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create or update UserAdditionalInfo for the user_profile
    additional_info, created = UserAdditionalInfo.objects.get_or_create(user_profile=user_profile)

    # Serialize the data from the request and update the UserAdditionalInfo instance
    serializer = UserAdditionalInfoSerializer(additional_info, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# content/models.py
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.template.defaulttags import now
from django.utils import timezone


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    description = models.TextField()

    def __str__(self):
        return self.title

class ZyraxTestimonial(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='testimonials/')
    description = models.TextField()
    tag = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Testimonials"
        verbose_name_plural = "Testimonials"


class CallbackRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    preferred_callback_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Callback Request from {self.name}"


class Offer(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount in percentage
    duration = models.IntegerField(default=30, help_text="Duration of the offer in days")  # Default 30 days
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='zyrax_user_profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username  # Return the username as the string representation


class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    content = models.TextField(blank=True)  # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the post is created

    def __str__(self):
        return f"{self.user.username}'s post on {self.created_at}"


# Image Model for Community Posts
class PostImage(models.Model):
    post = models.ForeignKey(CommunityPost, related_name='images', on_delete=models.CASCADE)  # Link to community post
    image = models.ImageField(upload_to='posts/')  # Store images in media/posts/

    def __str__(self):
        return f"Image for post {self.post.id}"


# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(CommunityPost,  on_delete=models.CASCADE, related_name='zyrax_comments')  # Link to community post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment is created

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class Zyrax_Class(models.Model):
    title = models.CharField(max_length=255)
    time = models.TimeField()
    duration = models.PositiveIntegerField()  # duration in minutes
    zoom_link = models.URLField()
    class_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Classes"  # This will display 'Banner' instead of 'Zylo_Banner'
        verbose_name_plural = "Classes"  # This will display 'Banners' in plural form (optional)


class Service_Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='service/')
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Services"
        verbose_name_plural = "Services"


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zyrax_attendance')
    date = models.DateField(default=timezone.now)  # Automatically set to today's date
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')  # Ensure one entry per user per day
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Tutors(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='tutorImage/')
    video_link = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Tutor Profile"
        verbose_name_plural = "Tutors Profile"


class UserAdditionalInfo(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='additional_info')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Height in cm
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Weight in kg
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_profile.user.username}'s Additional Info"



# Payment webhook
class PatymentRecord(models.Model):
    txnid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    payment_mode = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    upi_va = models.CharField(max_length=100, null=True, blank=True)
    addedon = models.DateTimeField(default=timezone.now)  # Set default to now
    bank_ref_num = models.CharField(max_length=100, null=True, blank=True)
    easepayid = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    productinfo = models.CharField(max_length=255, null=True, blank=True)
    service_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_amount_debit = models.DecimalField(max_digits=10, decimal_places=2)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cash_back_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.txnid} - {self.status}"

#
# class UserMembership(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
#     transaction_id = models.CharField(max_length=100, unique=True)
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
#     start_date = models.DateTimeField(default=now)
#     end_date = models.DateTimeField()
#     is_active = models.BooleanField(default=True)
#
#     def save(self, *args, **kwargs):
#         if not self.end_date:
#             self.end_date = self.start_date + timedelta(days=self.offer.duration)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.user} - {self.offer.title}"


class ActiveSubscribersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(end_date__gte=now(), is_active=True)

class InactiveSubscribersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(end_date__lt=now())  # Expired subscriptions

class UserMembership(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    objects = models.Manager()  # Default manager
    active_subscribers = ActiveSubscribersManager()
    inactive_subscribers = InactiveSubscribersManager()

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.offer.duration)
        # Auto-deactivate if expired
        if self.end_date < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.offer.title}"

class ActiveUserMembership(UserMembership):
    class Meta:
        proxy = True
        verbose_name = "Active Subscriber"
        verbose_name_plural = "Active Subscribers"

class InactiveUserMembership(UserMembership):
    class Meta:
        proxy = True
        verbose_name = "Inactive Subscriber"
        verbose_name_plural = "Inactive Subscribers"


# class Video(models.Model):
#     title = models.CharField(max_length=255)
#     video_link = models.URLField(max_length=500)
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.title
class Video(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)  # ✅ Title is optional
    video_link = models.URLField(max_length=500)
    description = models.TextField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title if self.title else "Untitled Video"  # Handle NULL title display


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


# class OTP(models.Model):
#     phone_number = models.CharField(max_length=15, unique=True)
#     otp = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def is_valid(self):
#         return (now() - self.created_at).seconds < 300  # 5 minutes

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link rating to a user
    score = models.IntegerField()  # Rating score between 1-5
    description = models.TextField(blank=True, null=True)  # New description field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.score} - {self.description[:20]}"
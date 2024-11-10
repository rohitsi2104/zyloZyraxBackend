from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# from django.contrib.auth.models import User

class Zylo_Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Banner"  # This will display 'Banner' instead of 'Zylo_Banner'
        verbose_name_plural = "Banners"  # This will display 'Banners' in plural form (optional)


class Zylo_Offer(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount in percentage
    duration = models.IntegerField(default=30, help_text="Duration of the offer in days")  # Default 30 days
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Offers"  # This will display 'Banner' instead of 'Zylo_Banner'
        verbose_name_plural = "Offers"  # This will display 'Banners' in plural form (optional)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='zylo_user_profile')  # Link to the User model
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.user.username  # Return the username as the string representation


class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zylo_community_post')  # Link to user
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
class Comments(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='zylo_comments')  # Link to community post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment is created

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"


class Zylo_Class(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zylo_attendance')
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

# content/models.py

from django.db import models
from django.contrib.auth.models import User

class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    description = models.TextField()

    def __str__(self):
        return self.title

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()

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
    post = models.ForeignKey(CommunityPost, related_name='comments', on_delete=models.CASCADE)  # Link to community post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to user
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment is created

    def __str__(self):
        return f"Comment by {self.user.username} on post {self.post.id}"
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Banner, Offer, CommunityPost, PostImage, Comment, UserProfile, Zyrax_Class, Tutors, Service_Post, ZyraxTestimonial, CallbackRequest, PatymentRecord


# Custom user creation form
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user


# Custom user admin to handle user registration
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserCreationForm
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # Remove the password from the fieldsets to avoid showing it
        return fieldsets


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Assuming 'title' and 'description' exist in the Banner model

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'preferred_callback_time', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('preferred_callback_time', 'created_at')
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'amount', 'discount', 'duration', 'is_active')  # Ensure 'is_active' is a field in the Zylo_Offer model

@admin.register(ZyraxTestimonial)
class ZyraxTestimonialAsmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(Zyrax_Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'duration', 'zoom_link', 'class_date')

@admin.register(Tutors)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'description')

@admin.register(Service_Post)
class Service_PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(PatymentRecord)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('txnid', 'amount', 'status', 'payment_mode', 'email', 'phone', 'addedon')
    search_fields = ('txnid', 'email', 'phone')
    list_filter = ('status', 'payment_mode', 'addedon')


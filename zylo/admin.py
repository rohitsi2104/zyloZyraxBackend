
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Zylo_Banner, Zylo_Offer


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


@admin.register(Zylo_Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Assuming 'title' and 'description' exist in the Banner model


@admin.register(Zylo_Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'discount', 'duration', 'is_active')  # Ensure 'is_active' is a field in the Zylo_Offer model


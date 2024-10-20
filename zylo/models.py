from django.db import models


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

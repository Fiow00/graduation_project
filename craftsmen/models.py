from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


CustomUser = get_user_model()

GOVERNORATE_CHOICES = [
    ('cairo', 'Cairo'),
    ('alexandria', 'Alexandria'),
    ('giza', 'Giza'),
    ('sharkia', 'Sharkia'),
    ('dakahlia', 'Dakahlia'),
    ('beheira', 'Beheira'),
    ('qalyubia', 'Qalyubia'),
    ('monufia', 'Monufia'),
    ('gharbia', 'Gharbia'),
    ('sohag', 'Sohag'),
    ('aswan', 'Aswan'),
    ('luxor', 'Luxor'),
    ('ismailia', 'Ismailia'),
    ('port_said', 'Port Said'),
    ('suez', 'Suez'),
    ('damietta', 'Damietta'),
    ('kafr_el_sheikh', 'Kafr El Sheikh'),
    ('matrouh', 'Matrouh'),
    ('north_sinai', 'North Sinai'),
    ('south_sinai', 'South Sinai'),
    ('red_sea', 'Red Sea'),
    ('new_valley', 'New Valley'),
    ('faiyum', 'Faiyum'),
    ('beni_suef', 'Beni Suef'),
    ('minya', 'Minya'),
    ('assiut', 'Assiut'),
    ('qena', 'Qena'),
]

class Craftsman(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(upload_to="craftsmen", blank=True, null=True)
    service = models.ForeignKey(
        'services.Service',
        related_name='craftsmen',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    bio = models.TextField(blank=True, null=True)
    governorate = models.CharField(max_length=50,choices=GOVERNORATE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    # Add to Craftsman model:
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # For avg ratings
    is_verified = models.BooleanField(default=False)  # Admin-approved craftsmen
    followers = models.ManyToManyField(get_user_model(), related_name='followed_craftsmen', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "craftsmen"
        ordering = ["-rating"]


class BookingRequest(models.Model):
    craftsman = models.ForeignKey('Craftsman', on_delete=models.CASCADE, related_name='booking_requests')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='booking_requests')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking from {self.user} to {self.craftsman} ({self.status})"


class Comment(models.Model):
    craftsman = models.ForeignKey(Craftsman, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,  # Remove default=timezone.now
        null=True,
        blank=True
    )
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-created_at']

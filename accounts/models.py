from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

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

EGYPT_PHONE_REGEX = r'^(\+20|0)?1[0-9]{9}$'

class CustomUser(AbstractUser): # table for users
    is_craftsman = models.BooleanField(default=False)
    phone = models.CharField(
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=EGYPT_PHONE_REGEX,
                message="Phone number must be Egyptian (e.g.: +201234567890, 01234567890, or 1234567890)"
            )
        ],
        help_text="Enter Egyptian number (e.g.: +201234567890 or 01234567890)"
    )
    photo = models.ImageField(upload_to="users", blank=True, null=True)
    governorate = models.CharField(max_length=50,choices=GOVERNORATE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Users"

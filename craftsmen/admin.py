from django.contrib import admin
from .models import Craftsman

class CraftsmanAdmin(admin.ModelAdmin):
    model = Craftsman
    list_display = ('user', 'service', 'governorate', 'city', 'experience_years')


admin.site.register(Craftsman, CraftsmanAdmin)

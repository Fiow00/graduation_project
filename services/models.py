import uuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class Service(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="services/",
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Upload image in JPG, PNG, or WEBP format"
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while Service.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={'slug': self.slug})  # Updated to use slug

    class Meta:
        db_table = "services"
        ordering = ['title']
        verbose_name = "Service"
        verbose_name_plural = "Services"

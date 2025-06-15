from django.urls import path
from .views import (
    ServiceListView, 
    ServiceDetailView, 
    ServiceViewSet, 
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("services", ServiceViewSet, basename="services")

urlpatterns = [
    path("", ServiceListView.as_view(), name="service_list"),
    path("<uuid:pk>/", ServiceDetailView.as_view(), name="service_detail"),
] + router.urls

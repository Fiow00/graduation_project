from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CraftsmanViewSet, CraftsmanDetailView

router = SimpleRouter()
router.register("craftsmen", CraftsmanViewSet, basename="craftsmen")

urlpatterns = [
    path("<int:pk>/", CraftsmanDetailView.as_view(), name="craftsman_detail"),
] + router.urls
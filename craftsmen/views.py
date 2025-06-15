from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Craftsman, Comment, BookingRequest
from .serializers import CraftsmanSerializer
from django.views.generic import DetailView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg

class CraftsmanViewSet(viewsets.ModelViewSet):
    queryset = Craftsman.objects.select_related('user', 'service').all()
    serializer_class = CraftsmanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Safer default

    def get_queryset(self):
        # Allow filtering by governorate/service via ?governorate=cairo&service=1
        queryset = super().get_queryset()
        if self.request.query_params.get('governorate'):
            queryset = queryset.filter(
                governorate=self.request.query_params.get('governorate')
            )
        # Add more filters as needed
        return queryset


class CraftsmanDetailView(DetailView):
    model = Craftsman
    template_name = "craftsmen/craftsman_detail.html"
    context_object_name = "craftsman"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        craftsman = self.object
        user = self.request.user
        context["comments"] = getattr(craftsman, "comments", None).all() if hasattr(craftsman, "comments") else []
        context["follower_count"] = craftsman.followers.count() if hasattr(craftsman, "followers") else 0
        average = craftsman.comments.aggregate(avg=Avg('rating'))['avg']
        context["average_rating"] = average
        context["is_following"] = False
        if user.is_authenticated and hasattr(craftsman, "followers"):
            context["is_following"] = craftsman.followers.filter(pk=user.pk).exists()
        # Booking logic
        context["has_pending_booking"] = False
        if user.is_authenticated and user != craftsman.user:
            context["has_pending_booking"] = BookingRequest.objects.filter(
                craftsman=craftsman, user=user, status='pending'
            ).exists()
        # Show received requests if craftsman is viewing their own profile
        if user.is_authenticated and user == craftsman.user:
            context["received_bookings"] = craftsman.booking_requests.select_related('user').order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        # Handle follow/unfollow
        if "follow" in request.POST and user.is_authenticated:
            if self.object.followers.filter(pk=user.pk).exists():
                self.object.followers.remove(user)
            else:
                self.object.followers.add(user)
            return redirect(reverse("craftsman_detail", kwargs={"pk": self.object.pk}))
        # Handle booking
        if "book" in request.POST and user.is_authenticated and user != self.object.user:
            if not BookingRequest.objects.filter(craftsman=self.object, user=user, status='pending').exists():
                BookingRequest.objects.create(
                    craftsman=self.object,
                    user=user,
                    message=request.POST.get("booking_message", "")
                )
            return redirect(reverse("craftsman_detail", kwargs={"pk": self.object.pk}))
        # Handle booking accept/refuse (for craftsman)
        if "accept_booking" in request.POST and user == self.object.user:
            booking_id = request.POST.get("accept_booking")
            BookingRequest.objects.filter(pk=booking_id, craftsman=self.object).update(status='accepted')
            return redirect(reverse("craftsman_detail", kwargs={"pk": self.object.pk}))
        if "refuse_booking" in request.POST and user == self.object.user:
            booking_id = request.POST.get("refuse_booking")
            BookingRequest.objects.filter(pk=booking_id, craftsman=self.object).update(status='refused')
            return redirect(reverse("craftsman_detail", kwargs={"pk": self.object.pk}))
        # Handle comment/rating
        if user.is_authenticated:
            comment_text = request.POST.get("comment")
            rating = request.POST.get("rating")
            if comment_text and rating:
                Comment.objects.create(
                    craftsman=self.object,
                    author=user,
                    comment=comment_text,
                    rating=rating
                )
        return redirect(reverse("craftsman_detail", kwargs={"pk": self.object.pk}))
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import get_user_model
from craftsmen.models import Craftsman, BookingRequest
from django.shortcuts import get_object_or_404
from .forms import UserProfileUpdateForm, CraftsmanProfileUpdateForm
from django.contrib import messages

CustomUser = get_user_model()

# Create your views here.
class HomepageView(TemplateView):
    template_name = "pages/home.html"

class AboutpageView(TemplateView):
    template_name = "pages/about.html"

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'craftsman'):
            return redirect('craftsman_profile')
        else:
            return redirect('user_profile')

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "pages/profiles/user_profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Pass the logged-in user to the template
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileUpdateForm
    template_name = "pages/profiles/user_profile_update.html"
    success_url = reverse_lazy('user_profile')

    def get_object(self):
        return self.request.user

class CraftsmanProfileView(LoginRequiredMixin, TemplateView):
    template_name = "pages/profiles/craftsman_profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the craftsman profile for the logged-in user
        craftsman = get_object_or_404(Craftsman, user=self.request.user)
        context['craftsman'] = craftsman

        return context

class CraftsmanProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Craftsman
    form_class = CraftsmanProfileUpdateForm
    template_name = "pages/profiles/craftsman_profile_update.html"
    success_url = reverse_lazy('craftsman_profile')

    def get_object(self):
        return self.request.user.craftsman


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_craftsman = hasattr(user, 'craftsman')
        context['is_craftsman'] = is_craftsman
        if is_craftsman:
            context['received_bookings'] = BookingRequest.objects.filter(
                craftsman=user.craftsman
            ).select_related('user').order_by('-created_at')
        else:
            context['bookings'] = BookingRequest.objects.filter(
                user=user
            ).select_related('craftsman__user').order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'craftsman'):
            if "accept_booking" in request.POST:
                booking_id = request.POST.get("accept_booking")
                BookingRequest.objects.filter(pk=booking_id, craftsman=user.craftsman).update(status='accepted')
            if "refuse_booking" in request.POST:
                booking_id = request.POST.get("refuse_booking")
                BookingRequest.objects.filter(pk=booking_id, craftsman=user.craftsman).update(status='refused')
        return redirect('dashboard')


class ContactUsView(TemplateView):
    template_name = "pages/contact_us.html"

    def post(self, request, *args, **kwargs):
        # You can process the form here (send email, save to DB, etc.)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Example: just show a success message (implement your own logic as needed)
        messages.success(request, "Thank you for contacting us! We will get back to you soon.")
        return self.get(request, *args, **kwargs)

class HelpCenterView(TemplateView):
    template_name = "pages/help_center.html"

class PrivacyPolicyView(TemplateView):
    template_name = "pages/privacy_policy.html"

class TermsOfServiceView(TemplateView):
    template_name = "pages/terms_of_service.html"

class FAQView(TemplateView):
    template_name = "pages/faq.html"

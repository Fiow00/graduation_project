from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

urlpatterns = [
    path("about/", views.AboutpageView.as_view(), name="about"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path('contact/', views.ContactUsView.as_view(), name='contact_us'),
    path('help-center/', views.HelpCenterView.as_view(), name='help_center'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("user_profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("user_profile/update/", views.UserProfileUpdateView.as_view(), name="user_profile_update"),
    path("craftsman_profile/", views.CraftsmanProfileView.as_view(), name="craftsman_profile"),
    path("craftsman_profile/update/", views.CraftsmanProfileUpdateView.as_view(), name="craftsman_profile_update"),
    path("", views.HomepageView.as_view(), name="home"),
]
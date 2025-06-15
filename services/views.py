from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Service
from .forms import ServiceForm
from django.db.models import Q
from rest_framework import viewsets
from .serializers import ServiceSerializer
from craftsmen.models import Craftsman
from django.shortcuts import get_object_or_404, render

# Create your views here.
class ServiceListView(ListView): # display all services in the database
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )
        return queryset

class ServiceDetailView(DetailView): # display only one service and all craftsmen doing this service
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['craftsmen'] = Craftsman.objects.filter(
            service=self.object,
            is_verified=True  # Assuming you added verification
        ).select_related('user')
        return context



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


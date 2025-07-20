from rest_framework import generics,status,filters
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.utils import timezone
from django.db.models import Q,Count,Avg
from datetime import timedelta
import logging


from .models import (
    GrazingZone, TrackingDevice, AnimalLocation,
    GeofenceEvent, NotificationContact, NotificationLog,
    AnimalGrazingAssignment
)
from .serializers import (
    GrazingZoneSerializer, GrazingZoneGeoSerializer,
    TrackingDeviceSerializer, AnimalLocationSerializer,
    AnimalLocationGeoSerializer, GeofenceEventSerializer,
    NotificationContactSerializer, NotificationLogSerializer,
    AnimalGrazingAssignmentSerializer,
    DeviceStatusUpdateSerializer
)

from animals.models import Animal

logger = logging.getLogger(__name__)


# Create your views here.
class GrazingZoneListCreateView(generics.ListCreateAPIView):
    """List and create grazing zones"""
    queryset = GrazingZone.objects.all()
    serializer_class = GrazingZoneSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['zone_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'zone_type']
    ordering = ['name']

class GrazingZoneDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete grazing zones"""
    queryset = GrazingZone.objects.all()
    serializer_class = GrazingZoneSerializer

class GrazingZoneGeoView(generics.ListAPIView):
    """GeoJSON endpoint for mapping applications"""
    queryset = GrazingZone.objects.filter(is_active=True)
    serializer_class = GrazingZoneGeoSerializer

class TrackingDeviceListCreateView(generics.ListCreateAPIView):
    """List and create tracking device"""
    queryset = TrackingDevice.objects.select_related('animal').all()
    serializer_class = TrackingDeviceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['device_type', 'status', 'manufacturer']
    search_fields = ['device_id', 'animal__tag_id', 'animal__name']
    ordering_fields = ['device_id', 'created_at', 'assigned_date']
    ordering = ['-created_at']


class TrackingDeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, and delete tracking devices"""
    queryset = TrackingDevice.objects.select_related('animal').all()
    serializer_class = TrackingDeviceSerializer

    def perform_update(self, serializer):
        """Set assigned_date when animal is assigned"""
        if 'animal' in serializer.validated_data and serializer.validated_data['animal']:
            if not self.get_object().animal or self.get_object().animal != serializer.validated_data['animal']:
                serializer.save(assigned_date=timezone.now())
            else:
                serializer.save()
        else:
            serializer.save()


class AnimalLocationListCreateView(generics.ListCreateAPIView):
    """List and create animal location records"""
    queryset = AnimalLocation.objects.select_related('animal', 'device').prefetch_related('inside_zones').all()
    serializer_class = AnimalLocationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['animal', 'device', 'is_within_boundary']
    ordering_fields = ['recorded_at', 'created_at']
    ordering = ['-recorded_at']

    def get_queryset(self):
        """Filter by date range and animal if specified"""
        queryset = super().get_queryset()

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(recorded_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(recorded_at__lte=end_date)

        # Get recent locations only by default (last 24 hours)
        if not start_date and not end_date:
            cutoff_time = timezone.now() - timedelta(hours=24)
            queryset = queryset.filter(recorded_at__gte=cutoff_time)

        return queryset


class AnimalLocationDetailView(generics.RetrieveAPIView):
    """Retrieve specific animal location record"""
    queryset = AnimalLocation.objects.select_related('animal', 'device').prefetch_related('inside_zones').all()
    serializer_class = AnimalLocationSerializer


class AnimalLocationGeoView(generics.ListAPIView):
    """GeoJSON endpoint for animal locations"""
    queryset = AnimalLocation.objects.select_related('animal').all()
    serializer_class = AnimalLocationGeoSerializer

    def get_queryset(self):
        """Get latest locations for each animal"""
        # Get most recent location for each animal
        latest_locations = AnimalLocation.objects.values('animal').annotate(
            latest_time=models.Max('recorded_at')
        )

        location_ids = []
        for item in latest_locations:
            location = AnimalLocation.objects.filter(
                animal=item['animal'],
                recorded_at=item['latest_time']
            ).first()
            if location:
                location_ids.append(location.id)

        return AnimalLocation.objects.filter(id__in=location_ids).select_related('animal')


class AnimalLocationDetailView(generics.RetrieveAPIView):
    """Retrieve specific animal location record"""
    queryset = AnimalLocation.objects.select_related('animal', 'device').prefetch_related('inside_zones').all()
    serializer_class = AnimalLocationSerializer


class AnimalLocationGeoView(generics.ListAPIView):
    """GeoJSON endpoint for animal locations"""
    queryset = AnimalLocation.objects.select_related('animal').all()
    serializer_class = AnimalLocationGeoSerializer

    def get_queryset(self):
        """Get latest locations for each animal"""
        # Get most recent location for each animal
        latest_locations = AnimalLocation.objects.values('animal').annotate(
            latest_time=models.Max('recorded_at')
        )

        location_ids = []
        for item in latest_locations:
            location = AnimalLocation.objects.filter(
                animal=item['animal'],
                recorded_at=item['latest_time']
            ).first()
            if location:
                location_ids.append(location.id)

        return AnimalLocation.objects.filter(id__in=location_ids).select_related('animal')
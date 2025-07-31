# tracking/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
import math

from .models import TrackingDevice, LocationUpdate, GeofenceZone, GeofenceAlert
from .serializers import (
    TrackingDeviceSerializer, LocationUpdateSerializer,
    LocationUpdateCreateSerializer, GeofenceZoneSerializer, GeofenceAlertSerializer
)


class TrackingDeviceViewSet(viewsets.ModelViewSet):
    queryset = TrackingDevice.objects.all()
    serializer_class = TrackingDeviceSerializer

    @action(detail=True, methods=['get'])
    def current_location(self, request, pk=None):
        """Get the most recent location for a device"""
        device = self.get_object()
        latest_location = device.location_updates.first()
        if latest_location:
            serializer = LocationUpdateSerializer(latest_location)
            return Response(serializer.data)
        return Response({'detail': 'No location data available'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def location_history(self, request, pk=None):
        """Get location history for a device with optional time filtering"""
        device = self.get_object()
        hours = request.query_params.get('hours', 24)

        try:
            hours = int(hours)
            since = timezone.now() - timedelta(hours=hours)
            locations = device.location_updates.filter(timestamp__gte=since)
            serializer = LocationUpdateSerializer(locations, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid hours parameter'}, status=status.HTTP_400_BAD_REQUEST)


class LocationUpdateViewSet(viewsets.ModelViewSet):
    queryset = LocationUpdate.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return LocationUpdateCreateSerializer
        return LocationUpdateSerializer

    def create(self, request, *args, **kwargs):
        """Create a new location update and check geofences"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location_update = serializer.save()

        # Check geofences after creating location update
        self._check_geofences(location_update)

        # Return the created location with full details
        response_serializer = LocationUpdateSerializer(location_update)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def _check_geofences(self, location_update):
        """Check if the location update triggers any geofence alerts"""
        active_zones = GeofenceZone.objects.filter(is_active=True)

        for zone in active_zones:
            distance = self._calculate_distance(
                float(location_update.latitude), float(location_update.longitude),
                float(zone.center_latitude), float(zone.center_longitude)
            )

            is_inside = distance <= zone.radius

            # Get the last alert for this device and zone
            last_alert = GeofenceAlert.objects.filter(
                device=location_update.device,
                zone=zone
            ).first()

            # Determine if we need to create an alert
            should_alert = False
            alert_type = None

            if is_inside and (not last_alert or last_alert.alert_type == 'EXIT'):
                should_alert = True
                alert_type = 'ENTER'
            elif not is_inside and (last_alert and last_alert.alert_type == 'ENTER'):
                should_alert = True
                alert_type = 'EXIT'

            if should_alert:
                GeofenceAlert.objects.create(
                    device=location_update.device,
                    zone=zone,
                    alert_type=alert_type,
                    location_update=location_update
                )

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points using Haversine formula"""
        R = 6371000  # Earth's radius in meters

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent location updates across all devices"""
        minutes = request.query_params.get('minutes', 30)
        try:
            minutes = int(minutes)
            since = timezone.now() - timedelta(minutes=minutes)
            locations = self.queryset.filter(timestamp__gte=since)
            serializer = self.get_serializer(locations, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid minutes parameter'}, status=status.HTTP_400_BAD_REQUEST)


class GeofenceZoneViewSet(viewsets.ModelViewSet):
    queryset = GeofenceZone.objects.all()
    serializer_class = GeofenceZoneSerializer

    @action(detail=True, methods=['get'])
    def animals_inside(self, request, pk=None):
        """Get animals currently inside this geofence zone"""
        zone = self.get_object()

        # Get latest location for each active device
        devices_inside = []
        active_devices = TrackingDevice.objects.filter(is_active=True)

        for device in active_devices:
            latest_location = device.location_updates.first()
            if latest_location:
                distance = self._calculate_distance(
                    float(latest_location.latitude), float(latest_location.longitude),
                    float(zone.center_latitude), float(zone.center_longitude)
                )
                if distance <= zone.radius:
                    devices_inside.append({
                        'device_id': device.device_id,
                        'animal_name': device.animal.name,
                        'animal_id': device.animal.id,
                        'distance_from_center': round(distance, 2)
                    })

        return Response(devices_inside)

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two points using Haversine formula"""
        R = 6371000  # Earth's radius in meters

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) * math.sin(delta_lon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c


class GeofenceAlertViewSet(viewsets.ModelViewSet):
    queryset = GeofenceAlert.objects.all()
    serializer_class = GeofenceAlertSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        acknowledged = self.request.query_params.get('acknowledged')

        if acknowledged is not None:
            if acknowledged.lower() == 'true':
                queryset = queryset.filter(is_acknowledged=True)
            elif acknowledged.lower() == 'false':
                queryset = queryset.filter(is_acknowledged=False)

        return queryset

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        """Mark an alert as acknowledged"""
        alert = self.get_object()
        alert.is_acknowledged = True
        alert.save()
        serializer = self.get_serializer(alert)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unacknowledged(self, request):
        """Get all unacknowledged alerts"""
        alerts = self.queryset.filter(is_acknowledged=False)
        serializer = self.get_serializer(alerts, many=True)
        return Response(serializer.data)
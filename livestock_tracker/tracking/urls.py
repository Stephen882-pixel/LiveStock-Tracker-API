from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrackingDeviceViewSet, LocationUpdateViewSet,
    GeofenceZoneViewSet, GeofenceAlertViewSet
)

router = DefaultRouter()
router.register(r'devices', TrackingDeviceViewSet)
router.register(r'locations', LocationUpdateViewSet)
router.register(r'geofences', GeofenceZoneViewSet)
router.register(r'alerts', GeofenceAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

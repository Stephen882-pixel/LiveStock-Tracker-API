from django.contrib import admin
from .models import TrackingDevice, LocationUpdate, GeofenceZone, GeofenceAlert

@admin.register(TrackingDevice)
class TrackingDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'animal', 'device_type', 'is_active', 'battery_level', 'last_seen']
    list_filter = ['device_type', 'is_active', 'last_seen']
    search_fields = ['device_id', 'animal__name']
    readonly_fields = ['last_seen', 'created_at']

@admin.register(LocationUpdate)
class LocationUpdateAdmin(admin.ModelAdmin):
    list_display = ['device', 'latitude', 'longitude', 'timestamp', 'accuracy']
    list_filter = ['device', 'timestamp']
    search_fields = ['device__device_id', 'device__animal__name']
    readonly_fields = ['created_at']
    ordering = ['-timestamp']

@admin.register(GeofenceZone)
class GeofenceZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'zone_type', 'center_latitude', 'center_longitude', 'radius', 'is_active']
    list_filter = ['zone_type', 'is_active']
    search_fields = ['name']

@admin.register(GeofenceAlert)
class GeofenceAlertAdmin(admin.ModelAdmin):
    list_display = ['device', 'zone', 'alert_type', 'is_acknowledged', 'created_at']
    list_filter = ['alert_type', 'is_acknowledged', 'created_at']
    search_fields = ['device__device_id', 'zone__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
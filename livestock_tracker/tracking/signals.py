from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import LocationUpdate, GeofenceAlert, TrackingDevice
from .serializers import LocationUpdateSerializer, GeofenceAlertSerializer

channel_layer = get_channel_layer()


@receiver(post_save, sender=LocationUpdate)
def broadcast_location_update(sender, instance, created, **kwargs):
    """Broadcast new location updates via WebSocket"""
    if created:
        # Prepare location data
        location_data = {
            'id': instance.id,
            'device_id': instance.device.device_id,
            'animal_id': instance.device.animal.id,
            'animal_name': instance.device.animal.name,
            'latitude': float(instance.latitude),
            'longitude': float(instance.longitude),
            'altitude': instance.altitude,
            'accuracy': instance.accuracy,
            'speed': instance.speed,
            'timestamp': instance.timestamp.isoformat()
        }

        # Broadcast to general tracking group
        async_to_sync(channel_layer.group_send)(
            "live_tracking",
            {
                "type": "location_update",
                "data": location_data
            }
        )

        # Broadcast to specific animal subscribers
        async_to_sync(channel_layer.group_send)(
            f"animal_{instance.device.animal.id}",
            {
                "type": "location_update",
                "data": location_data
            }
        )


@receiver(post_save, sender=GeofenceAlert)
def broadcast_geofence_alert(sender, instance, created, **kwargs):
    """Broadcast new geofence alerts via WebSocket"""
    if created:
        # Prepare alert data
        alert_data = {
            'id': instance.id,
            'device_id': instance.device.device_id,
            'animal_id': instance.device.animal.id,
            'animal_name': instance.device.animal.name,
            'zone_id': instance.zone.id,
            'zone_name': instance.zone.name,
            'zone_type': instance.zone.zone_type,
            'alert_type': instance.alert_type,
            'latitude': float(instance.location_update.latitude),
            'longitude': float(instance.location_update.longitude),
            'is_acknowledged': instance.is_acknowledged,
            'created_at': instance.created_at.isoformat()
        }

        # Broadcast to general tracking group
        async_to_sync(channel_layer.group_send)(
            "live_tracking",
            {
                "type": "geofence_alert",
                "data": alert_data
            }
        )

        # Broadcast to specific animal subscribers
        async_to_sync(channel_layer.group_send)(
            f"animal_{instance.device.animal.id}",
            {
                "type": "geofence_alert",
                "data": alert_data
            }
        )


@receiver(pre_save, sender=TrackingDevice)
def track_device_changes(sender, instance, **kwargs):
    """Track changes to device status for broadcasting"""
    if instance.pk:  # Only for existing devices
        try:
            old_instance = TrackingDevice.objects.get(pk=instance.pk)
            instance._old_battery_level = old_instance.battery_level
            instance._old_is_active = old_instance.is_active
        except TrackingDevice.DoesNotExist:
            pass


@receiver(post_save, sender=TrackingDevice)
def broadcast_device_status_update(sender, instance, created, **kwargs):
    """Broadcast device status changes via WebSocket"""
    if not created:  # Only for updates, not new devices
        battery_changed = getattr(instance, '_old_battery_level', None) != instance.battery_level
        status_changed = getattr(instance, '_old_is_active', None) != instance.is_active

        if battery_changed or status_changed:
            # Prepare device status data
            device_data = {
                'device_id': instance.device_id,
                'animal_id': instance.animal.id,
                'animal_name': instance.animal.name,
                'battery_level': instance.battery_level,
                'is_active': instance.is_active,
                'last_seen': instance.last_seen.isoformat() if instance.last_seen else None,
                'changes': {
                    'battery_changed': battery_changed,
                    'status_changed': status_changed
                }
            }

            # Broadcast to general tracking group
            async_to_sync(channel_layer.group_send)(
                "live_tracking",
                {
                    "type": "device_status_update",
                    "data": device_data
                }
            )

            # Broadcast to specific animal subscribers
            async_to_sync(channel_layer.group_send)(
                f"animal_{instance.animal.id}",
                {
                    "type": "device_status_update",
                    "data": device_data
                }
            )
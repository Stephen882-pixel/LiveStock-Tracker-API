import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from datetime import timedelta
from .models import TrackingDevice, LocationUpdate, GeofenceAlert
from .serializers import LocationUpdateSerializer, GeofenceAlertSerializer


class LiveTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the general tracking group
        await self.channel_layer.group_add("live_tracking", self.channel_name)
        await self.accept()

        # Send initial data when client connects
        await self.send_initial_data()

    async def disconnect(self, close_code):
        # Leave the tracking group
        await self.channel_layer.group_discard("live_tracking", self.channel_name)

    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'subscribe_animal':
                animal_id = data.get('animal_id')
                if animal_id:
                    await self.subscribe_to_animal(animal_id)

            elif message_type == 'unsubscribe_animal':
                animal_id = data.get('animal_id')
                if animal_id:
                    await self.unsubscribe_from_animal(animal_id)

            elif message_type == 'get_recent_locations':
                minutes = data.get('minutes', 30)
                await self.send_recent_locations(minutes)

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))

    async def subscribe_to_animal(self, animal_id):
        """Subscribe to updates for a specific animal"""
        group_name = f"animal_{animal_id}"
        await self.channel_layer.group_add(group_name, self.channel_name)

        # Send current location for this animal
        location_data = await self.get_animal_current_location(animal_id)
        if location_data:
            await self.send(text_data=json.dumps({
                'type': 'current_location',
                'animal_id': animal_id,
                'data': location_data
            }))

    async def unsubscribe_from_animal(self, animal_id):
        """Unsubscribe from updates for a specific animal"""
        group_name = f"animal_{animal_id}"
        await self.channel_layer.group_discard(group_name, self.channel_name)

    async def send_initial_data(self):
        """Send initial tracking data when client connects"""
        # Send active devices
        devices = await self.get_active_devices()
        await self.send(text_data=json.dumps({
            'type': 'active_devices',
            'data': devices
        }))

        # Send recent unacknowledged alerts
        alerts = await self.get_unacknowledged_alerts()
        if alerts:
            await self.send(text_data=json.dumps({
                'type': 'unacknowledged_alerts',
                'data': alerts
            }))

    async def send_recent_locations(self, minutes):
        """Send recent locations for all animals"""
        locations = await self.get_recent_locations(minutes)
        await self.send(text_data=json.dumps({
            'type': 'recent_locations',
            'data': locations
        }))

    # WebSocket message handlers (called by group_send)
    async def location_update(self, event):
        """Handle location update broadcast"""
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'data': event['data']
        }))

    async def geofence_alert(self, event):
        """Handle geofence alert broadcast"""
        await self.send(text_data=json.dumps({
            'type': 'geofence_alert',
            'data': event['data']
        }))

    async def device_status_update(self, event):
        """Handle device status update broadcast"""
        await self.send(text_data=json.dumps({
            'type': 'device_status_update',
            'data': event['data']
        }))

    # Database query methods
    @database_sync_to_async
    def get_active_devices(self):
        """Get all active tracking devices"""
        devices = TrackingDevice.objects.filter(is_active=True).select_related('animal')
        return [{
            'device_id': device.device_id,
            'animal_id': device.animal.id,
            'animal_name': device.animal.name,
            'battery_level': device.battery_level,
            'last_seen': device.last_seen.isoformat() if device.last_seen else None
        } for device in devices]

    @database_sync_to_async
    def get_unacknowledged_alerts(self):
        """Get recent unacknowledged geofence alerts"""
        alerts = GeofenceAlert.objects.filter(
            is_acknowledged=False
        ).select_related('device__animal', 'zone', 'location_update')[:10]

        return [{
            'id': alert.id,
            'device_id': alert.device.device_id,
            'animal_name': alert.device.animal.name,
            'zone_name': alert.zone.name,
            'alert_type': alert.alert_type,
            'latitude': float(alert.location_update.latitude),
            'longitude': float(alert.location_update.longitude),
            'created_at': alert.created_at.isoformat()
        } for alert in alerts]

    @database_sync_to_async
    def get_recent_locations(self, minutes):
        """Get recent location updates"""
        since = timezone.now() - timedelta(minutes=minutes)
        locations = LocationUpdate.objects.filter(
            timestamp__gte=since
        ).select_related('device__animal').order_by('-timestamp')[:50]

        return [{
            'id': loc.id,
            'device_id': loc.device.device_id,
            'animal_id': loc.device.animal.id,
            'animal_name': loc.device.animal.name,
            'latitude': float(loc.latitude),
            'longitude': float(loc.longitude),
            'altitude': loc.altitude,
            'accuracy': loc.accuracy,
            'speed': loc.speed,
            'timestamp': loc.timestamp.isoformat()
        } for loc in locations]

    @database_sync_to_async
    def get_animal_current_location(self, animal_id):
        """Get current location for a specific animal"""
        try:
            device = TrackingDevice.objects.get(animal_id=animal_id, is_active=True)
            latest_location = device.location_updates.first()
            if latest_location:
                return {
                    'device_id': device.device_id,
                    'animal_id': animal_id,
                    'animal_name': device.animal.name,
                    'latitude': float(latest_location.latitude),
                    'longitude': float(latest_location.longitude),
                    'altitude': latest_location.altitude,
                    'accuracy': latest_location.accuracy,
                    'speed': latest_location.speed,
                    'timestamp': latest_location.timestamp.isoformat()
                }
        except TrackingDevice.DoesNotExist:
            pass
        return None
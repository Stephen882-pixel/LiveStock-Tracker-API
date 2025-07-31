from rest_framework import serializers
from .models import TrackingDevice, LocationUpdate, GeofenceZone, GeofenceAlert


class TrackingDeviceSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    animal_id = serializers.IntegerField(source='animal.id', read_only=True)

    class Meta:
        model = TrackingDevice
        fields = ['id', 'device_id', 'device_type', 'animal', 'animal_name',
                  'animal_id', 'is_active', 'battery_level', 'last_seen', 'created_at']
        read_only_fields = ['last_seen', 'created_at']


class LocationUpdateSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source='device.device_id', read_only=True)
    animal_name = serializers.CharField(source='device.animal.name', read_only=True)

    class Meta:
        model = LocationUpdate
        fields = ['id', 'device', 'device_id', 'animal_name', 'latitude',
                  'longitude', 'altitude', 'accuracy', 'speed', 'timestamp', 'created_at']
        read_only_fields = ['created_at']


class LocationUpdateCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating location updates via device_id"""
    device_id = serializers.CharField(write_only=True)

    class Meta:
        model = LocationUpdate
        fields = ['device_id', 'latitude', 'longitude', 'altitude', 'accuracy', 'speed', 'timestamp']

    def create(self, validated_data):
        device_id = validated_data.pop('device_id')
        try:
            device = TrackingDevice.objects.get(device_id=device_id, is_active=True)
            validated_data['device'] = device
            return super().create(validated_data)
        except TrackingDevice.DoesNotExist:
            raise serializers.ValidationError({'device_id': 'Invalid or inactive device ID'})


class GeofenceZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeofenceZone
        fields = ['id', 'name', 'zone_type', 'center_latitude', 'center_longitude',
                  'radius', 'is_active', 'created_at']
        read_only_fields = ['created_at']


class GeofenceAlertSerializer(serializers.ModelSerializer):
    device_id = serializers.CharField(source='device.device_id', read_only=True)
    animal_name = serializers.CharField(source='device.animal.name', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    latitude = serializers.DecimalField(source='location_update.latitude', max_digits=10, decimal_places=8,
                                        read_only=True)
    longitude = serializers.DecimalField(source='location_update.longitude', max_digits=11, decimal_places=8,
                                         read_only=True)

    class Meta:
        model = GeofenceAlert
        fields = ['id', 'device', 'device_id', 'animal_name', 'zone', 'zone_name',
                  'alert_type', 'latitude', 'longitude', 'is_acknowledged', 'created_at']
        read_only_fields = ['created_at']
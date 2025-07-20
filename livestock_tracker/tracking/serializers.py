from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.gis.geos import Point
from django.utils import timezone
from .models import (
    GrazingZone,TrackingDevice,AnimalLocation,
    GeofenceEvent,NotificationContact,NotificationLog,
    AnimalGrazingAssignment
)
from animals.models import Animal
from animals.serializers import AnimalListSerializer


class GrazingZoneSerializer(serializers.ModelSerializer):
    """Serializer for GrazingZone model"""
    animal_count = serializers.SerializerMethodField()
    active_animal_count = serializers.SerializerMethodField()


    class Meta:
        model = GrazingZone
        fields = ['id','name','zone_type','description','boundary','center_point','radius_meters','is_active',
                  'max_capacity','access_start_time','access_end_time','created_at','updated_at','animals_count',
                  'active_animals_count']

    def get_animals_count(self,obj):
        """Get total number of animals assigned to this zone"""
        return obj.animal_assignments.filter(is_active=True).count()

    def get_active_animals_count(self,obj):
        """Get number of animals currently in this zone"""
        return AnimalLocation.objects.filter(
            inside_zones = obj,
            recorded_at__gte=timezone.now() - timezone.timedelta(hours=1)
        ).values('animal').distinct().count()

class GrazingZoneGeoSerializer(GeoFeatureModelSerializer):
    """GeoJson serializer for mapping applications"""
    animal_count = serializers.SerializerMethodField()

    class Meta:
        model = GrazingZone
        geo_field = "boundary"
        fields = [
            'id','name','zone_type','description','is_active',
            'max_capacity','animals_count'
        ]

        def get_animals_count(self,obj):
            return obj.animal_assignments.filter(is_active=True).count()


class TrackingDeviceSerializer(serializers.ModelSerializer):
    """Serializer for TrackingDevice model"""
    animal_name = serializers.CharField(source='animal.name',read_only=True)
    animal_tag_id = serializers.CharField(source='animal.tag_id',read_only=True)
    days_since_assigned = serializers.SerializerMethodField()


    class Meta:
        model = TrackingDevice
        fields = [
            'id','device_id','device_type','manufacturer','model','battery_life_days','update_interval_minutes',
            'accuracy_meters','status','last_battery_level','last_signal_strength','animal','animal_name','animal_tag_id',
            'assigned_date','days_since_assigned','created_at','updated_at'
        ]
        read_only_fields =  [
            'last_battery_level', 'last_signal_strength'
        ]

    def get_days_since_assigned(self,obj):
        """Calculate days since device was assigned to current animal"""
        if obj.assigned_date:
            return (timezone.now() - obj.assigned_date).days
        return None

    def validate_animal(self,value):
        """Ensure animal does not already have a tracking device"""
        if value and hasattr(value,'tracking_device') and value.tracking_device != self.instance:
            raise serializers.ValidationError(
                f"Animal {value.tag_id} alread has a tracking device assigned."
            )
        return value

class AnimalLocationSerializer(serializers.ModelSerializer):
    """Serializers for recieving GPS location updates"""
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    animal_tag_id = serializers.CharField(source='animal.tag_id',read_only=True)
    device_id = serializers.CharField(source='device.device_id',read_only=True)
    zone_names = serializers.SerializerMethodField()

    class Meta:
        model = AnimalLocation
        fields = [
            'id', 'animal', 'device', 'animal_tag_id', 'device_id',
            'latitude', 'longitude', 'location', 'altitude', 'accuracy',
            'speed', 'heading', 'battery_level', 'signal_strength',
            'temperature', 'inside_zones', 'zones_names', 'is_within_boundary',
            'recorded_at', 'created_at'
        ]
        read_only_fields = ['location', 'inside_zones', 'is_within_boundary', 'created_at']


    def get_zone_names(self,obj):
        """Get names of zones where animal is currently located"""
        return [zone.name for zone in obj.inside_zones.all()]

    def create(self, validated_data):
        """Create location record with geospatial processing"""
        latitude = validated_data.pop('latitude')
        longitude = validated_data('longitude')

        # Create Point geometry
        location_point = Point(longitude, latitude)
        validated_data['location'] = location_point

        # Create the location record
        location_record = AnimalLocation.objects.create(**validated_data)

        # Process geofencing after creation
        self._process_geofencing(location_record)

        # Update device status
        self._update_device_status(location_record)

        return location_record

    def _process_geofencing(self, location_record):
        """Process geofencing logic"""
        from .utils import check_geofence_status
        check_geofence_status(location_record)

    def _update_device_status(self, location_record):
        """Update device with latest readings"""
        device = location_record.device
        if location_record.battery_level is not None:
            device.last_battery_level = location_record.battery_level
        if location_record.signal_strength is not None:
            device.last_signal_strength = location_record.signal_strength
        device.save(update_fields=['last_battery_level', 'last_signal_strength', 'updated_at'])


class AnimalLocationGeoSerializer(GeoFeatureModelSerializer):
    """GeoJSON serializer for location data"""
    animal_tag_id = serializers.CharField(source='animal.tag_id', read_only=True)
    animal_name = serializers.CharField(source='animal.name', read_only=True)

    class Meta:
        model = AnimalLocation
        geo_field = "location"
        fields = [
            'id', 'animal_tag_id', 'animal_name', 'battery_level',
            'signal_strength', 'speed', 'heading', 'recorded_at'
        ]
class GeofenceEventSerializer(serializers.ModelSerializer):
    """Serializer for GeofenceEvent model"""
    animal_tag_id = serializers.CharField(source='animal.tag_id', read_only=True)
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model = GeofenceEvent
        fields = [
            'id', 'event_id', 'animal', 'animal_tag_id', 'animal_name',
            'zone', 'zone_name', 'location_record', 'event_type',
            'event_type_display', 'severity', 'severity_display',
            'distance_from_boundary', 'duration_outside', 'notes',
            'created_at'
        ]
        read_only_fields = ['event_id', 'created_at']


class NotificationContactSerializer(serializers.ModelSerializer):
    """Serializer for NotificationContact model"""
    animals_count = serializers.SerializerMethodField()
    contact_type_display = serializers.CharField(source='get_contact_type_display', read_only=True)

    class Meta:
        model = NotificationContact
        fields = [
            'id', 'name', 'contact_type', 'contact_type_display',
            'phone_number', 'email', 'preferred_methods',
            'notification_hours_start', 'notification_hours_end',
            'animals', 'animals_count', 'is_active',
            'created_at', 'updated_at'
        ]

    def get_animals_count(self, obj):
        """Get count of animals associated with this contact"""
        return obj.animals.filter(status='active').count()

    def validate_phone_number(self, value):
        """Validate phone number format for Africa's Talking"""
        if not value.startswith('+'):
            raise serializers.ValidationError(
                "Phone number must include country code (e.g., +254...)"
            )
        return value

    def validate_preferred_methods(self, value):
        """Validate preferred notification methods"""
        valid_methods = dict(NotificationContact.NOTIFICATION_METHOD_CHOICES).keys()
        for method in value:
            if method not in valid_methods:
                raise serializers.ValidationError(
                    f"'{method}' is not a valid notification method. "
                    f"Valid options: {list(valid_methods)}"
                )
        return value

class NotificationLogSerializer(serializers.ModelSerializer):
    """Serializer for NotificationLog model"""
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    contact_phone = serializers.CharField(source='contact.phone_number', read_only=True)
    event_details = serializers.CharField(source='geofence_event.get_event_type_display', read_only=True)
    animal_tag_id = serializers.CharField(source='geofence_event.animal.tag_id', read_only=True)

    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification_id', 'geofence_event', 'contact',
            'contact_name', 'contact_phone', 'animal_tag_id',
            'event_details', 'method', 'message', 'at_message_id',
            'at_session_id', 'cost', 'status', 'sent_at',
            'delivered_at', 'failed_reason', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'notification_id', 'at_message_id', 'at_session_id',
            'sent_at', 'delivered_at', 'created_at', 'updated_at'
        ]


class AnimalGrazingAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for AnimalGrazingAssignment model"""
    animal_tag_id = serializers.CharField(source='animal.tag_id', read_only=True)
    animal_name = serializers.CharField(source='animal.name', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    zone_type = serializers.CharField(source='zone.zone_type', read_only=True)

    class Meta:
        model = AnimalGrazingAssignment
        fields = [
            'id', 'animal', 'animal_tag_id', 'animal_name',
            'zone', 'zone_name', 'zone_type', 'is_active',
            'notes', 'created_at', 'updated_at'
        ]

    def validate(self, data):
        """Validate that animal-zone assignment doesn't already exist"""
        animal = data.get('animal')
        zone = data.get('zone')
        is_active = data.get('is_active', True)

        if is_active and animal and zone:
            existing = AnimalGrazingAssignment.objects.filter(
                animal=animal,
                zone=zone,
                is_active=True
            )
            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError(
                    f"Animal {animal.tag_id} is already assigned to zone {zone.name}"
                )

        return data


class DeviceStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating device status from external systems"""
    device_id = serializers.CharField()
    battery_level = serializers.IntegerField(min_value=0, max_value=100, required=False)
    signal_strength = serializers.IntegerField(required=False)
    status = serializers.ChoiceField(choices=TrackingDevice.STATUS_CHOICES, required=False)

    def validate_device_id(self, value):
        """Validate that device exists"""
        try:
            TrackingDevice.objects.get(device_id=value)
        except TrackingDevice.DoesNotExist:
            raise serializers.ValidationError(f"Device with ID '{value}' does not exist")
        return value

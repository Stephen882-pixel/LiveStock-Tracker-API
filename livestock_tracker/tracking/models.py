from django.db import models
from django.utils import timezone
from animals.models import Animal


# Create your models here.

class TrackingDevice(models.Model):
    device_id = models.CharField(max_length=50,unique=True)
    device_type = models.CharField(max_length=20,default='GPS_COLLAR')
    animal = models.OneToOneField(Animal,on_delete=models.CASCADE,related_name='tracking_device')
    is_active = models.BooleanField(default=True)
    battery_level = models.IntegerField(default=100) # percentage
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device {self.device_id} - {self.animal}"


class LocationUpdate(models.Model):
    device = models.ForeignKey(TrackingDevice, on_delete=models.CASCADE, related_name='location_updates')
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    altitude = models.FloatField(null=True, blank=True)  # meters above sea level
    accuracy = models.FloatField(default=0.0)  # GPS accuracy in meters
    speed = models.FloatField(null=True, blank=True)  # km/h
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.device.device_id} at {self.latitude}, {self.longitude} - {self.timestamp}"


class GeofenceZone(models.Model):
    ZONE_TYPES = [
        ('PASTURE', 'Pasture'),
        ('FEEDING', 'Feeding Area'),
        ('WATER', 'Water Source'),
        ('RESTRICTED', 'Restricted Area'),
        ('SAFE', 'Safe Zone'),
    ]

    name = models.CharField(max_length=100)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPES)
    # Simple circular geofence for prototype
    center_latitude = models.DecimalField(max_digits=10, decimal_places=8)
    center_longitude = models.DecimalField(max_digits=11, decimal_places=8)
    radius = models.FloatField()  # radius in meters
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.zone_type})"


class GeofenceAlert(models.Model):
    ALERT_TYPES = [
        ('ENTER', 'Entered Zone'),
        ('EXIT', 'Exited Zone'),
    ]

    device = models.ForeignKey(TrackingDevice, on_delete=models.CASCADE)
    zone = models.ForeignKey(GeofenceZone, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    location_update = models.ForeignKey(LocationUpdate, on_delete=models.CASCADE)
    is_acknowledged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.device.device_id} {self.alert_type} {self.zone.name}"
from django.db import models
from django.contrib.gis.db import  models as gis_models
from django.contrib.gis.geos import Point, Polygon
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
from decimal import  Decimal
import  uuid
from livestock_tracker.animals.models import Animal

# Create your models here.

class GrazingZone(models.Model):
    """Defines geo-fenced grazing areas for livestock"""
    ZONE_TYPE_CHOICES = [
        ("grazing","Grazing Area"),
        ("watering","Watering Point"),
        ("shelter","Shelter point"),
        ("restricted","Restricted Area"),
        ("quarantine","Quarantine ZOne")
    ]

    name = models.CharField(max_length=200)
    zone_type = models.CharField(max_length=20,choices=ZONE_TYPE_CHOICES,default="grazing")
    description = models.TextField(blank=True)

    # Geospatial boundary - can be circle or polygon
    boundary = gis_models.PolygonField(help_text="Zone boundary coordinates")
    center_point = gis_models.PointField(null=True,blank=True,help_text="Center of the zone")
    radius_meters = models.IntegerField(null=True,blank=True,help_text="Radius is meters(for circular zones)")

    # Zone settings
    is_active = models.BooleanField(default=True)
    max_capacity = models.IntegerField(null=True,blank=True,help_text="Maximum number of animals")


    # Time based restrictions
    access_start_time = models.TimeField(null=True,blank=True,help_text="Daily access start time")
    access_end_time = models.TimeField(null=True,blank=True,help_text="Daily access end time")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"


class TrackingDevice(models.Model):
    """Represents GPS tracking devices attached to animals"""
    DEVICE_TYPE_CHOICES = [
        ("gps_collar","GPS Collar"),
        ("ear tag","GPS Ear Tag"),
        ("ankle_band","GPS Ankle Band"),
        ("implant","GPS Implant")
    ]

    STATUS_CHOICES = [
        ("active","Active"),
        ("inactive","Inactive"),
        ('maintenance', 'Under Maintenance'),
        ('lost', 'Lost/Damaged'),
    ]

    device_id = models.CharField(max_length=100,unique=True,help_text="Unique device identifier")
    device_type = models.CharField(max_length=20,choices=DEVICE_TYPE_CHOICES)
    manufacturer = models.CharField(max_length=100,blank=true)
    model = models.CharField(max_length=100,blank=True)

    # Device specifications
    battery_life_days = models.IntegerField(null=True,blank=True)
    update_interval_minutes = models.IntegerField(default=15,help_text="GPS update frequency in minutes")
    accuracy_meters = models.IntegerField(null=True,blank=True,help_text="GPS accuracy in meters")

    # Current status
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="active")
    last_battery_level = models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0),MaxValueValidator(100)])
    last_signal_strength = models.IntegerField(null=True,blank=True,help_text="Signal strength_percentage")

    # Assignment
    animal = models.OneToOneField(Animal,on_delete=models.SET_NULL,null=True,blank=True,related_name='tracking_device')
    assigned_date = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-device_id']

    def __str__(self):
        animal_name = self.animal.name if self.animal else "Unassigned"
        return f"{self.device_id} - {animal_name}"

class AnimalLocation(models.Model):
    """Stores GPS location data for animals"""
    animal = models.ForeignKey(Animal,on_delete=models.CASCADE,related_name="locations")
    device = models.ForeignKey(TrackingDevice,on_delete=models.CASCADE,related_name='location_records')

    # Location data
    location = gis_models.PointField(help_text="GPS coordites")
    altitude = models.DecimalField(max_digits=8,decimal_places=2,null=True,blank=True,help_text="Altitude in meters")
    accuracy = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True,help_text="GPS Accuracy in meters")
    speed = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True,help_text="speed in km/h")
    heading = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True,help_text="Direction in degrees")

    # Device status at time of reading
    battery_level = models.IntegerField(null=True, blank=True,validators=[MinValueValidator(0), MaxValueValidator(100)])
    signal_strength = models.IntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,help_text="Device temperature in Celsius")

    # Geo-fence status
    inside_zones = models.ManyToManyField(GrazingZone, blank=True, help_text="Zones where animal is currently located")
    is_within_boundary = models.BooleanField(default=True,help_text="Whether animal is within any assigned grazing zone")

    recorded_at = models.DateTimeField(help_text="When the GPS reading was taken")
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the record was stored in database")


    class Meta:
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['animal','-recorded_at']),
            models.Index(fields=['device','recorded_at']),
            models.Index(fields=['-recorded_at']),
        ]

    def __str__(self):
        return f"{self.animal.tag_id} - {self.recorded_at}"

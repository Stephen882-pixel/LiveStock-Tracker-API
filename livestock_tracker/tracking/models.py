from django.db import models
from django.contrib.gis.db import  models as gis_models
from django.contrib.gis.geos import Point, Polygon
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
from decimal import  Decimal
import  uuid

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

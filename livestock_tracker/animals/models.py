from django.db import models
from django.core.validators import MinValueValidator
from datetime import date

# Create your models here.
class Breed(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    origin_country = models.CharField(max_length=100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Animal(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female','Female')
    ]

    HEALTH_STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('sick', 'Sick'),
        ('under_treatment', 'Under Treatment'),
        ('recovering', 'Recovering'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('sold', 'Sold'),
        ('deceased', 'Deceased'),
    ]

    tag_id = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    breed = models.ForeignKey(Breed,on_delete=models.CASCADE,related_name='animals')
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Weight in Kilograms"
    )
    color = models.CharField(max_length=50,blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='active')
    location = models.CharField(max_length=200,blank=True,null=True)
    health_status = models.CharField(max_length=20,choices=HEALTH_STATUS_CHOICES,default='healthy')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tag_id} - {self.name}"

    @property
    def age_in_days(self):
        """Calculate age in days"""
        return (date.today() - self.date_of_birth).days

    @property
    def age_in_years(self):
        """Calculate age in years"""
        return self.age_in_days // 365




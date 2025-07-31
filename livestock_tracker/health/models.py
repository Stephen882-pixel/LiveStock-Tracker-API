from django.db import models



class HealthEvent(models.Model):
    EVENT_TYPES = [
        ('vaccination', 'Vaccination'),
        ('treatment', 'Treatment'),
        ('checkup', 'Health Checkup'),
        ('illness', 'Illness'),
        ('injury', 'Injury'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    animal_id = models.IntegerField()  # Reference to your animal model
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='low')
    event_date = models.DateTimeField()
    veterinarian = models.CharField(max_length=100, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return f"{self.title} - Animal {self.animal_id}"


class Vaccination(models.Model):
    animal_id = models.IntegerField()
    vaccine_name = models.CharField(max_length=100)
    vaccine_type = models.CharField(max_length=50)
    administered_date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    batch_number = models.CharField(max_length=50, blank=True)
    veterinarian = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-administered_date']

    def __str__(self):
        return f"{self.vaccine_name} - Animal {self.animal_id}"


class Treatment(models.Model):
    TREATMENT_STATUS = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('discontinued', 'Discontinued'),
    ]

    animal_id = models.IntegerField()
    condition = models.CharField(max_length=200)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TREATMENT_STATUS, default='ongoing')
    veterinarian = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.medication} for {self.condition} - Animal {self.animal_id}"
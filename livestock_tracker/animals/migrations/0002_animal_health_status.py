# Generated by Django 4.2.7 on 2025-07-19 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='health_status',
            field=models.CharField(choices=[('healthy', 'Healthy'), ('sick', 'Sick'), ('under_treatment', 'Under Treatment'), ('recovering', 'Recovering')], default='healthy', max_length=20),
        ),
    ]

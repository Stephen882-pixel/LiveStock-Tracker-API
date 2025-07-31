from rest_framework import serializers
from .models import HealthEvent, Vaccination, Treatment


class HealthEventSerializer(serializers.ModelSerializer):
    #created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = HealthEvent
        fields = [
            'id', 'animal_id', 'event_type', 'title', 'description', 
            'severity', 'event_date', 'veterinarian', 'cost', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    # def create(self, validated_data):
    #     validated_data['created_by'] = self.context['request'].user
    #     return super().create(validated_data)


class VaccinationSerializer(serializers.ModelSerializer):
    #created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    days_until_due = serializers.SerializerMethodField()
    
    class Meta:
        model = Vaccination
        fields = [
            'id', 'animal_id', 'vaccine_name', 'vaccine_type', 
            'administered_date', 'next_due_date', 'batch_number',
            'veterinarian', 'cost', 'notes',
            'created_at', 'days_until_due'
        ]
        read_only_fields = ['created_at']

    def get_days_until_due(self, obj):
        if obj.next_due_date:
            from django.utils import timezone
            today = timezone.now().date()
            delta = obj.next_due_date - today
            return delta.days
        return None

    # def create(self, validated_data):
    #     validated_data['created_by'] = self.context['request'].user
    #     return super().create(validated_data)


class TreatmentSerializer(serializers.ModelSerializer):
    #created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = Treatment
        fields = [
            'id', 'animal_id', 'condition', 'medication', 'dosage',
            'frequency', 'start_date', 'end_date', 'status',
            'veterinarian', 'cost', 'notes', 
            'created_at', 'updated_at', 'duration_days'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_duration_days(self, obj):
        if obj.end_date:
            delta = obj.end_date - obj.start_date
            return delta.days
        return None

    # def create(self, validated_data):
    #     validated_data['created_by'] = self.context['request'].user
    #     return super().create(validated_data)
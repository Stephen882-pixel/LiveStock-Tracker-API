from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta

from .models import HealthEvent, Vaccination, Treatment
from .serializers import HealthEventSerializer, VaccinationSerializer, TreatmentSerializer
from .filters import HealthEventFilter


class HealthEventViewSet(viewsets.ModelViewSet):
    serializer_class = HealthEventSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HealthEventFilter
    search_fields = ['title', 'description', 'veterinarian']
    ordering_fields = ['event_date', 'created_at', 'severity']
    ordering = ['-event_date']

    def get_queryset(self):
        return HealthEvent.objects.all()

    @action(detail=False, methods=['get'])
    def by_animal(self, request):
        """Get health events for a specific animal"""
        animal_id = request.query_params.get('animal_id')
        if not animal_id:
            return Response({'error': 'animal_id parameter is required'}, status=400)
        
        events = self.get_queryset().filter(animal_id=animal_id)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent health events (last 30 days)"""
        thirty_days_ago = timezone.now() - timedelta(days=30)
        events = self.get_queryset().filter(event_date__gte=thirty_days_ago)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


class VaccinationViewSet(viewsets.ModelViewSet):
    serializer_class = VaccinationSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_id', 'vaccine_type']
    search_fields = ['vaccine_name', 'veterinarian']
    ordering_fields = ['administered_date', 'next_due_date']
    ordering = ['-administered_date']

    def get_queryset(self):
        return Vaccination.objects.all()

    @action(detail=False, methods=['get'])
    def due_soon(self, request):
        """Get vaccinations due in the next 30 days"""
        thirty_days_ahead = timezone.now().date() + timedelta(days=30)
        vaccinations = self.get_queryset().filter(
            next_due_date__lte=thirty_days_ahead,
            next_due_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(vaccinations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_animal(self, request):
        """Get vaccinations for a specific animal"""
        animal_id = request.query_params.get('animal_id')
        if not animal_id:
            return Response({'error': 'animal_id parameter is required'}, status=400)
        
        vaccinations = self.get_queryset().filter(animal_id=animal_id)
        serializer = self.get_serializer(vaccinations, many=True)
        return Response(serializer.data)


class TreatmentViewSet(viewsets.ModelViewSet):
    serializer_class = TreatmentSerializer
    #permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['animal_id', 'status']
    search_fields = ['condition', 'medication', 'veterinarian']
    ordering_fields = ['start_date', 'end_date']
    ordering = ['-start_date']

    def get_queryset(self):
        return Treatment.objects.all()

    @action(detail=False, methods=['get'])
    def ongoing(self, request):
        """Get ongoing treatments"""
        treatments = self.get_queryset().filter(status='ongoing')
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_animal(self, request):
        """Get treatments for a specific animal"""
        animal_id = request.query_params.get('animal_id')
        if not animal_id:
            return Response({'error': 'animal_id parameter is required'}, status=400)
        
        treatments = self.get_queryset().filter(animal_id=animal_id)
        serializer = self.get_serializer(treatments, many=True)
        return Response(serializer.data)
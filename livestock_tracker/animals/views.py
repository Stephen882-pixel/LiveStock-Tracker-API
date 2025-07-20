from rest_framework import generics,status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from  rest_framework.filters import SearchFilter,OrderingFilter
from .models import Animal,Breed
from .serializers import (
    AnimalListSerializer,
    AnimalCreateSerializer,
    AnimalDetailSerializer,
    BreedSerializer
)

# Create your views here.
class BreedListCreateView(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','description']
    ordering_fields = ["name","created_at"]
    ordering =  ["name"]

class BreedDetailVIews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class AnimalListCreateView(generics.ListCreateAPIView):
    queryset = Animal.objects.select_related('breed').all()
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = ['breed','gender','health_status']
    search_fields = ['tag_id','name','breed__name']
    ordering_fields = ['created_at', 'name', 'weight', 'date_of_birth']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnimalCreateSerializer
        return AnimalListSerializer


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.select_related('breed').all()

    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return AnimalCreateSerializer
        return AnimalDetailSerializer



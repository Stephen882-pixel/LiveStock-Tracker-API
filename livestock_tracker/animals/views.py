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
class BreedListSerializer(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','description']
    ordering_fields = ["name","created_at"]
    ordering =  ["name"]


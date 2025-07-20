from django.urls import  path
from .views import (
    AnimalListCreateView,
    AnimalDetailView,
    BreedListCreateView,
    BreedDetailViews
)


urlpatterns = [
    # Breed Urls
    path('breeds/',BreedListCreateView.as_view(),name='breed-list-create'),
    path('breeds/<int:pk>/',BreedDetailViews.as_view(),name='breed-detail'),

    #Anima URLS
    path('animals/',AnimalListCreateView.as_view(),name='animal-list-create'),
    path('animals/<int:pk>/',AnimalDetailView.as_view(),name='animal-detail')
]
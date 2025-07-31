from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.HealthEventViewSet, basename='healthevent')
router.register(r'vaccinations', views.VaccinationViewSet, basename='vaccination')
router.register(r'treatments', views.TreatmentViewSet, basename='treatment')

urlpatterns = [
    path('api/health/', include(router.urls)),
]
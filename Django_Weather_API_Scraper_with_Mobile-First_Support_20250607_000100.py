Title: Django Weather API Scraper with Mobile-First Support

```python
# Django project setup
# =====================
# Step 1: Create a new Django project and app
# - django-admin startproject WeatherScraper
# - cd WeatherScraper
# - django-admin startapp weather

# settings.py
# ===========
INSTALLED_APPS = [
    ...,
    'weather',  # Register the weather app
    'rest_framework',  # Add Django REST Framework for API handling
    'corsheaders',  # Handle CORS for API access on mobile devices
]

MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Example origin, can be set for mobile front-end app
    # Add other allowed origins like mobile app domains
]

# models.py
# =========
from django.db import models

class WeatherData(models.Model):
    # Define the weather data structure
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.temperature}C - {self.description}"

# serializers.py
# ==============
from rest_framework import serializers
from .models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'

# views.py
# ========
from rest_framework import viewsets
from rest_framework.response import Response
from .models import WeatherData
from .serializers import WeatherDataSerializer
import requests  # For API requests
from django.conf import settings

class WeatherDataViewSet(viewsets.ViewSet):
    """
    ViewSet for reading the weather data.
    Currently supports listing all entries in a mobile-first approach.
    """
    
    def list(self, request):
        queryset = WeatherData.objects.all()
        serializer = WeatherDataSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve_external_weather_data(self, location):
        """
        Fetch weather data from an external API.
        Replace API_URL and KEY with actual service endpoint.
        """
        API_URL = "https://api.example.com/weather"
        KEY = "YOUR_API_KEY"
        
        response = requests.get(API_URL, params={"q": location, "appid": KEY})
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not fetch data"}

# urls.py
# ========
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'weather', views.WeatherDataViewSet, basename='weatherdata')

urlpatterns = [
    path('', include(router.urls)),
]

# admin.py
# ========
from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('location', 'temperature', 'description', 'created_at')

# tasks.py (for periodic updates, if needed)
# ==========================================
from celery import shared_task
from .models import WeatherData
from .views import WeatherDataViewSet

@shared_task
def update_weather_data():
    """
    Task to update the weather data periodically.
    This requires Celery setup and a scheduler like Redis.
    Fetch and save data from an external API.
    """
    weather_view = WeatherDataViewSet()
    locations = ['New York', 'Los Angeles', 'London']
    
    for location in locations:
        data = weather_view.retrieve_external_weather_data(location)
        if 'error' not in data:
            WeatherData.objects.create(
                location=location,
                temperature=data['main']['temp'],
                description=data['weather'][0]['description']
            )
```

This setup assumes you will need to replace `'https://api.example.com/weather'` and the `'YOUR_API_KEY'` with the actual external weather API URL and API key, respectively. You also need to ensure you run a mobile-oriented front-end or application that is accessible within the listed `CORS_ALLOWED_ORIGINS`. Additionally, tasks using Celery and Redis in the `tasks.py` file are optional if periodic updates are needed.
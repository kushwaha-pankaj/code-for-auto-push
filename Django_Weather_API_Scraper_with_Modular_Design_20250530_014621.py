Title: Django Weather API Scraper with Modular Design

```python
# Create a new Django project named 'weather_project'
# (Run the following in your terminal, not part of the code)
# django-admin startproject weather_project

# Within the 'weather_project', create a new Django app named 'weather_scraper'
# (Run the following in your terminal, not part of the code)
# python manage.py startapp weather_scraper

# settings.py (located inside weather_project/weather_project/)
# Add 'weather_scraper' to the list of installed apps
INSTALLED_APPS = [
    # ...
    'weather_scraper',
]

# models.py (located inside weather_scraper/)
from django.db import models

# Define a Weather model to store weather data
class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}: {self.temperature}°C, {self.description}"


# services.py (create this file inside weather_scraper/)
import requests

# Function to fetch weather data from an external API
def fetch_weather_data(city):
    API_KEY = 'your_api_key'  # User must replace with their actual API key
    URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
        return weather_data
    else:
        # Handle error responses
        return None


# views.py (located inside weather_scraper/)
from django.http import JsonResponse
from .services import fetch_weather_data
from .models import Weather

# View to retrieve and save weather data
def get_weather(request, city):
    weather_data = fetch_weather_data(city)
    if weather_data:
        # Save the retrieved data to the database
        weather_record = Weather.objects.create(
            city=weather_data['city'],
            temperature=weather_data['temperature'],
            description=weather_data['description']
        )
        return JsonResponse({'message': 'Weather data retrieved and stored', 'data': weather_data})
    else:
        return JsonResponse({'error': 'Error fetching weather data'}, status=404)


# urls.py (located inside weather_scraper/)
from django.urls import path
from .views import get_weather

# Define the URL pattern for the weather scraper app
urlpatterns = [
    path('weather/<str:city>/', get_weather, name='get_weather'),
]

# urls.py (located inside weather_project/weather_project/)
from django.contrib import admin
from django.urls import path, include

# Include the weather_scraper app URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('weather_scraper.urls')),
]

# Run migrations to create Weather model in the database
# (Run the following in your terminal, not part of the code)
# python manage.py makemigrations weather_scraper
# python manage.py migrate

# To test, ensure Django server is running:
# python manage.py runserver
# Access the API endpoint by visiting http://127.0.0.1:8000/api/weather/<city>/
```

In this practice, we have created a modular Django application that scrapes weather data for a given city from an external weather API and saves it to a database. The application's structure is divided into models, views, services, and URL configurations for better modularity and maintainability.
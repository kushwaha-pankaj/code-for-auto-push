```python
# Title: Weather API Scraper using Django with Modular Design

# Django Imports
from django.core.management.base import BaseCommand
from django.conf import settings
import requests

# App Imports
from weather_scraper.models import WeatherData
from weather_scraper.utils import parse_weather_data, save_weather_data

# settings.py
# Add your Weather API Key and URL in Django settings
API_KEY = 'your_api_key_here'
API_URL = 'http://api.weatherapi.com/v1/current.json'

# models.py
from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    condition = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.location} - {self.temperature}°C - {self.condition}'

# utils.py
def fetch_weather_data(location):
    """Fetch weather data from the API for a given location."""
    params = {
        'key': settings.API_KEY,
        'q': location
    }
    response = requests.get(settings.API_URL, params=params)
    response.raise_for_status()
    return response.json()

def parse_weather_data(data):
    """Parse weather data from API response."""
    location = data['location']['name']
    temperature = data['current']['temp_c']
    condition = data['current']['condition']['text']
    return {
        'location': location,
        'temperature': temperature,
        'condition': condition
    }

def save_weather_data(data):
    """Save parsed weather data to the database."""
    weather_data, created = WeatherData.objects.update_or_create(
        location=data['location'],
        defaults={
            'temperature': data['temperature'],
            'condition': data['condition']
        }
    )
    return weather_data

# management/commands/scrape_weather.py
class Command(BaseCommand):
    help = 'Scrape weather data for a list of locations'

    def add_arguments(self, parser):
        parser.add_argument('location', nargs='+', type=str, help='List of locations to scrape weather data for')

    def handle(self, *args, **kwargs):
        locations = kwargs['location']
        for location in locations:
            self.stdout.write(f'Scraping weather data for {location}...')
            try:
                weather_data_json = fetch_weather_data(location)
                parsed_data = parse_weather_data(weather_data_json)
                save_weather_data(parsed_data)
                self.stdout.write(self.style.SUCCESS(f'Successfully updated weather for {location}'))
            except (requests.exceptions.RequestException, Exception) as e:
                self.stderr.write(self.style.ERROR(f'Error updating weather for {location}: {e}'))
```

This code sets up a Django-based weather API scraper using a modular design approach. It includes the integration of different components such as data fetching, parsing, and saving into a reusable and clean structure.
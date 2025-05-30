Title: Django Weather API Scraper with Input Validation

```python
# Import necessary libraries
import requests
from django.http import JsonResponse
from django.core.validators import int_list_validator
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json

# Define a simple function to validate the city name input
def validate_city_name(city_name):
    if not city_name.isalpha():
        raise ValidationError("City name must contain only alphabetic characters.")

# Create a Django view to handle the weather data
@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for simplicity
class WeatherView(View):
    def post(self, request):
        # Parse JSON request body
        data = json.loads(request.body)

        # Get city name from request and validate
        city_name = data.get('city', '')
        try:
            validate_city_name(city_name)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Construct the request URL for the weather API
        api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=YOUR_API_KEY_HERE'

        # Fetch data from the weather API
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Return the API response as JSON to the client
        return JsonResponse(response.json(), status=response.status_code)

# Example URL mapping for the above view
from django.urls import path

urlpatterns = [
    path('get_weather/', WeatherView.as_view(), name='get_weather'),
]

# To run this Django application, add the above urlpatterns to your project's urls.py
```

Ensure to replace `'YOUR_API_KEY_HERE'` with your actual API key from the OpenWeatherMap API service. This simple Django application defines a `WeatherView` to fetch weather data from the OpenWeatherMap API for a given city after validating the city name input for alphabetic characters only.
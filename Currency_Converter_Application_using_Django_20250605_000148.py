Title: Currency Converter Application using Django

```python
# Import necessary libraries and modules
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import path
from django.test import TestCase, Client
import requests

# Create your models here
# A simple model to store currency rates if needed (not used directly in this application)
class CurrencyRate(models.Model):
    currency_code = models.CharField(max_length=3, primary_key=True)
    rate_to_usd = models.FloatField()

# A function to handle the currency conversion logic
def convert_currency(amount, from_currency, to_currency):
    # Fetch the latest exchange rates from a public API
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()

    # Get the rate of the from-currency and to-currency
    from_rate = data['rates'].get(from_currency, None)
    to_rate = data['rates'].get(to_currency, None)
    
    # Calculate and return the converted amount
    if from_rate is None or to_rate is None:
        raise ValueError('Invalid currency code provided.')
    
    # Convert the amount to USD first, then to the target currency
    amount_in_usd = amount / from_rate
    converted_amount = amount_in_usd * to_rate
    
    return converted_amount

# Create a view to handle user requests
def convert_view(request):
    if request.method == 'GET':
        amount = float(request.GET.get('amount'))
        from_currency = request.GET.get('from_currency')
        to_currency = request.GET.get('to_currency')

        try:
            converted_amount = convert_currency(amount, from_currency, to_currency)
            response = {
                'success': True,
                'converted_amount': converted_amount
            }
        except ValueError as e:
            response = {
                'success': False,
                'error': str(e)
            }
    
        return JsonResponse(response)

# Define the URL patterns
urlpatterns = [
    path('convert/', convert_view),
]

# Unit tests for currency converter
class CurrencyConverterTests(TestCase):

    def setUp(self):
        # Set up the test client
        self.client = Client()

    def test_valid_conversion(self):
        # Test conversion with valid parameters
        response = self.client.get('/convert/', {'amount': 100, 'from_currency': 'EUR', 'to_currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_invalid_currency_code(self):
        # Test conversion with an invalid currency code
        response = self.client.get('/convert/', {'amount': 100, 'from_currency': 'XXX', 'to_currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
        self.assertIn('error', response.json())

    def test_invalid_amount(self):
        # Test conversion with a non-numeric amount
        with self.assertRaises(ValueError):
            convert_currency('invalid', 'USD', 'EUR')

# Note: Run these tests using Django's test runner.
```

This code provides a simple Django-based currency converter application. The main functionality is the conversion function `convert_currency`, which uses the exchange rates from a public API. There is a view `convert_view` that handles the GET request for converting currencies and the response in JSON format. Basic unit tests for valid and invalid scenarios are also included using Django's `TestCase`.
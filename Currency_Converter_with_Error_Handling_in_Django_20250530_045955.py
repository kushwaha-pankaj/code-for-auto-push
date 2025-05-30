Title: Currency Converter with Error Handling in Django

```python
# models.py

from django.db import models

class Currency(models.Model):
    # Model to store currency information
    code = models.CharField(max_length=3, unique=True)  # e.g., USD, EUR
    name = models.CharField(max_length=64)  # Full name of the currency

    def __str__(self):
        return self.code

class ExchangeRate(models.Model):
    # Model to store exchange rate information
    base_currency = models.ForeignKey(Currency, related_name='base_currency', on_delete=models.CASCADE)
    target_currency = models.ForeignKey(Currency, related_name='target_currency', on_delete=models.CASCADE)
    rate = models.FloatField()  # Exchange rate

    def __str__(self):
        return f"{self.base_currency} to {self.target_currency}"


# forms.py

from django import forms

class CurrencyConversionForm(forms.Form):
    # Form to handle currency conversion request
    amount = forms.FloatField(min_value=0.0, label='Amount')
    from_currency = forms.CharField(max_length=3, label='From Currency')
    to_currency = forms.CharField(max_length=3, label='To Currency')


# views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Currency, ExchangeRate
from .forms import CurrencyConversionForm

def convert_currency(request):
    # View to handle currency conversion
    if request.method == 'POST':
        form = CurrencyConversionForm(request.POST)
        if form.is_valid():
            try:
                from_currency = get_object_or_404(Currency, code=form.cleaned_data['from_currency'])
                to_currency = get_object_or_404(Currency, code=form.cleaned_data['to_currency'])
                amount = form.cleaned_data['amount']
                
                exchange_rate = get_object_or_404(ExchangeRate, base_currency=from_currency, target_currency=to_currency)
                
                converted_amount = amount * exchange_rate.rate
                response = {
                    'success': True,
                    'converted_amount': converted_amount
                }
            except Currency.DoesNotExist:
                response = {
                    'success': False,
                    'error': 'Currency not found'
                }
            except ExchangeRate.DoesNotExist:
                response = {
                    'success': False,
                    'error': 'Exchange rate not found'
                }
            except Exception as e:
                response = {
                    'success': False,
                    'error': str(e)
                }
        else:
            response = {
                'success': False,
                'error': form.errors.as_json()
            }
        return JsonResponse(response)
    
    # Render an empty form for GET requests
    form = CurrencyConversionForm()
    return render(request, 'currency_converter/form.html', {'form': form})


# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('convert/', views.convert_currency, name='convert_currency'),
]


# templates/currency_converter/form.html

<!DOCTYPE html>
<html>
<head>
    <title>Currency Converter</title>
</head>
<body>
    <h1>Currency Converter</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Convert</button>
    </form>
</body>
</html>

```

This Django application provides a simple currency converter with error handling. It consists of models to store currencies and exchange rates, forms for user input, views to handle logic and render templates, and basic error management while dealing with the database.
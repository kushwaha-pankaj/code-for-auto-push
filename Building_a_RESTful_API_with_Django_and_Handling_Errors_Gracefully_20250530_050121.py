Title: Building a RESTful API with Django and Handling Errors Gracefully

```python
# Importing necessary Django and DRF modules
from django.db import models
from django.urls import path
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound, ParseError
from django.core.validators import MinLengthValidator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Creating a simple model for demonstration
class Item(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    description = models.TextField()

# Serializer for the Item model
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

# A function to handle not found and bad request errors more gracefully
def error_response(message, status_code):
    return JsonResponse({'error': message}, status=status_code)

@api_view(['GET', 'POST'])
@method_decorator(csrf_exempt, name='dispatch')  # Disabling CSRF for simplicity
def item_list(request):
    # List all items or create a new item.
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            serializer = ItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ParseError:
            return error_response("Invalid JSON", status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@method_decorator(csrf_exempt, name='dispatch')
def item_detail(request, pk):
    # Retrieve, update or delete an item instance.
    try:
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return error_response("Item not found", status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        try:
            data = JSONParser().parse(request)
            serializer = ItemSerializer(item, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ParseError:
            return error_response("Invalid JSON", status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# URL configuration for the API
urlpatterns = [
    path('items/', item_list),
    path('items/<int:pk>/', item_detail),
]
```

This code sets up a basic Django application with a RESTful API for the `Item` model. It uses Django REST Framework to list, create, update, and delete items while handling errors gracefully. The functions `item_list` and `item_detail` include error handling for not found and invalid input cases, and JSON parsing errors are caught to provide cleaner error responses.
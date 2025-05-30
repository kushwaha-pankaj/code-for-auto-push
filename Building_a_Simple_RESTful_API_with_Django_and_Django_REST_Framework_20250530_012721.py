Title: Building a Simple RESTful API with Django and Django REST Framework

```python
# Importing necessary modules
from django.urls import path, include
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

# Defining a simple model for demonstration
class Item(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField()

    def __str__(self) -> str:
        return self.name

# Creating a serializer for the model
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']

# Defining a view set for the Item model
class ItemViewSet(viewsets.ViewSet):
    def list(self, request) -> Response:
        """List all items"""
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request) -> Response:
        """Create a new item"""
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk: int) -> Response:
        """Retrieve a single item by id"""
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk: int) -> Response:
        """Update an existing item"""
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk: int) -> Response:
        """Delete an item by id"""
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Setting up the router and URL configurations
router: DefaultRouter = DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

urlpatterns: list = [
    path('api/', include(router.urls)),
]

# Ensuring the CSRF token is exempted for the demonstration
@csrf_exempt
@api_view(['GET'])
def api_root(request) -> JsonResponse:
    """Welcome message for the API root"""
    return JsonResponse({'message': 'Welcome to the Item API'})
```

Note: This code assumes a Django project is already set up. You need to add the necessary Django REST Framework configuration in `settings.py` to make this work. The code structure is kept simple and straightforward, focusing on core RESTful operations.